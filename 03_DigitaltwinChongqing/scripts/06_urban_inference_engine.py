import os
import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio
from shapely.geometry import Point
from scipy.spatial import cKDTree

pd.options.mode.string_storage = 'python'

def extract_elevation_from_raster(gdf: gpd.GeoDataFrame, raster_path: str) -> np.ndarray:
    """Extrae el valor Z del raster para cada geometria del GeoDataFrame."""
    centroids = gdf.geometry.centroid
    coords = [(geom.x, geom.y) for geom in centroids]
    
    elevations = []
    try:
        with rasterio.open(raster_path) as src:
            for val in src.sample(coords):
                elevations.append(val[0])
    except Exception as e:
        print(f"Error al leer el raster: {e}")
        return np.zeros(len(gdf))
        
    return np.array(elevations)

def assign_building_heights(area: float, score: float) -> int:
    """
    Motor de decision para Chongqing.
    Asigna niveles basados en la huella de construccion y el puntaje espacial.
    """
    # Huellas pequeñas (< 400m2)
    if area < 400:
        if score > 70: return 8    # Pequeño comercio central
        else: return 3             # Vivienda autoconstruida/antigua
        
    # Huellas medias (400m2 - 1200m2) -> Tipico residencial Xiaoqu o Tongzilou
    elif 400 <= area < 1200:
        if score > 80: return 33   # Residencial alta densidad bien conectado
        elif score > 50: return 18 # Residencial estandar
        else: return 8             # Residencial antiguo periférico
        
    # Huellas masivas (> 1200m2) -> CBD, Malls, Torres
    else:
        if score > 85: return 65   # Rascacielos corporativo (CBD)
        elif score > 60: return 40 # Torre de uso mixto
        else: return 20            # Complejo comercial aislado
        
def process_inference_model(raw_dir: str, processed_dir: str) -> None:
    print("Iniciando el motor de inferencia espacial...")
    
    # 1. Carga de datos 
    crs_utm = 'EPSG:32648'
    
    print("Cargando capas base...")
    buildings = gpd.read_file(os.path.join(raw_dir, 'chongqingZ_overture_buildings.geojson'), engine='pyogrio').to_crs(crs_utm)
    pois = gpd.read_file(os.path.join(raw_dir, 'chongqingZ_pois.geojson'), engine='pyogrio').to_crs(crs_utm)
    roads = gpd.read_file(os.path.join(raw_dir, 'chongqingZ_road_hierarchy.geojson'), engine='pyogrio').to_crs(crs_utm)
    transit = gpd.read_file(os.path.join(raw_dir, 'chongqingZ_transit_nodes.geojson'), engine='pyogrio').to_crs(crs_utm)
    dem_path = os.path.join(raw_dir, 'chongqingZ_elevation_utm.tif')
    
    # 2. Extraccion de Elevaciones (Z)
    print("Extrayendo topografia...")
    buildings['elevation'] = extract_elevation_from_raster(buildings, dem_path)
    transit['elevation'] = extract_elevation_from_raster(transit, dem_path)
    
    # 3. Analisis Espacial: Distancia a Transporte con Penalizacion Topografica
    print("Calculando distancias equivalentes al transporte...")
    transit_tree = cKDTree(np.array(list(zip(transit.geometry.x, transit.geometry.y))))
    b_coords = np.array(list(zip(buildings.geometry.centroid.x, buildings.geometry.centroid.y)))
    
    # Distancia Euclidiana como aproximacion inicial rapida a la red
    dists, indices = transit_tree.query(b_coords)
    
    # Factor de correccion de red (Aproximacion de tortuosidad urbana = 1.3)
    network_dists = dists * 1.3 
    
    # Penalizacion por pendiente (1m de desnivel = 10m de esfuerzo horizontal)
    transit_elevs = transit.iloc[indices]['elevation'].values
    delta_z = np.abs(buildings['elevation'].values - transit_elevs)
    equivalent_dists = network_dists + (delta_z * 10)
    
    buildings['dist_transit_eq'] = equivalent_dists
    
    # 4. Analisis Espacial: Buffer de Comercio (POIs a 200m)
    print("Calculando densidad comercial...")
    poi_tree = cKDTree(np.array(list(zip(pois.geometry.x, pois.geometry.y))))
    poi_counts = poi_tree.query_ball_point(b_coords, r=200)
    buildings['poi_count_200m'] = [len(p) for p in poi_counts]
    
    # # 5. Analisis Espacial: Jerarquia Vial
    print("Asignando jerarquia vial...")
    
    hierarchy_weights = {'trunk': 100, 'primary': 80, 'secondary': 50, 'residential': 20}
    
    # Uso de indice espacial (R-tree) forzando un unico resultado por poligono
    centroids = buildings.geometry.centroid
    nearest_road_indices = roads.sindex.nearest(centroids, return_all=False)[1]
    
    nearest_road_types = roads.iloc[nearest_road_indices]['highway'].astype(str).str.lower().values
    buildings['road_weight'] = [hierarchy_weights.get(rt, 10) for rt in nearest_road_types]
    # 6. Motor de Puntaje (Scoring)
    print("Ejecutando inferencia de alturas...")
    # Normalizacion y calculo
    max_pois = buildings['poi_count_200m'].max() if buildings['poi_count_200m'].max() > 0 else 1
    
    scores = []
    for _, row in buildings.iterrows():
        # A. Score Transporte (cae a 0 despues de 500m equivalentes)
        t_score = max(0, (500 - row['dist_transit_eq']) / 5) 
        
        # B. Score POIs (Normalizado a 100)
        p_score = (row['poi_count_200m'] / max_pois) * 100
        
        # C. Score Vial
        r_score = row['road_weight']
        
        # Puntaje Final ponderado (0 - 100)
        final_score = (t_score * 0.4) + (p_score * 0.3) + (r_score * 0.3)
        scores.append(final_score)
        
    buildings['inference_score'] = scores
    
    # 7. Asignacion final de niveles y geometria
    buildings['area_sqm'] = buildings.geometry.area
    buildings['inferred_levels'] = buildings.apply(lambda x: assign_building_heights(x['area_sqm'], x['inference_score']), axis=1)
    buildings['inferred_height_m'] = buildings['inferred_levels'] * 3.0
    
    # Limpieza de columnas complejas para exportacion
    cols_to_keep = ['geometry', 'elevation', 'dist_transit_eq', 'poi_count_200m', 
                    'road_weight', 'inference_score', 'area_sqm', 'inferred_levels', 'inferred_height_m']
    buildings_export = buildings[cols_to_keep]
    
    output_path = os.path.join(processed_dir, 'chongqingZ_inferred_buildings.geojson')
    buildings_export.to_file(output_path, driver='GeoJSON', engine='pyogrio')
    print(f"Gemelo digital generado exitosamente. Archivo guardado en: {output_path}")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    PROCESSED_DIR = os.path.join(SCRIPT_DIR, '../data/processed')
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    process_inference_model(RAW_DIR, PROCESSED_DIR)