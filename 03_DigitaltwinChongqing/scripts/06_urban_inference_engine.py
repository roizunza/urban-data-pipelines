import os
import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio
from scipy.spatial import cKDTree

pd.options.mode.string_storage = 'python'

def extract_raster_values(gdf: gpd.GeoDataFrame, raster_path: str) -> np.ndarray:
    """
    Extrae valores de raster mediante indexacion de matriz.
    Incluye validacion estricta y reproyeccion dinamica para empatar el CRS del raster original.
    """
    vals = []
    try:
        with rasterio.open(raster_path) as src:
            raster_crs = src.crs
            
            # Reproyeccion temporal al vuelo si los CRS no coinciden
            if gdf.crs != raster_crs:
                gdf_temp = gdf.to_crs(raster_crs)
            else:
                gdf_temp = gdf
                
            centroids = gdf_temp.geometry.centroid
            data = src.read(1)
            
            for geom in centroids:
                try:
                    row, col = src.index(geom.x, geom.y)
                    # Validacion de limites de matriz
                    if 0 <= row < src.height and 0 <= col < src.width:
                        val = data[row, col]
                        vals.append(val if val > 0 else 0)
                    else:
                        vals.append(0)
                except Exception:
                    vals.append(0)
                    
    except Exception as e:
        print(f"Error critico en raster {raster_path}: {e}")
        return np.zeros(len(gdf))
        
    return np.array(vals)

def assign_building_heights(area: float, score: float) -> int:
    """
    Motor de decision para Chongqing.
    Umbrales ajustados a la distribucion estadistica local.
    """
    if area < 400:
        if score > 60: return 15
        else: return 3
        
    elif 400 <= area < 1500:
        if score > 60: return 45
        elif score > 40: return 25
        else: return 10
        
    elif 1500 <= area < 3000:
        if score > 60: return 75
        elif score > 45: return 45
        else: return 25
        
    else:
        if score > 60: return 110
        elif score > 45: return 65
        else: return 30
        
def process_inference_model(raw_dir: str, processed_dir: str) -> None:
    print("Iniciando el motor de inferencia espacial...")
    
    crs_utm = 'EPSG:32648'
    
    print("Cargando capas base...")
    buildings_path = os.path.join(processed_dir, '01_digitaltwin_buildings.geojson.geojson')
    buildings = gpd.read_file(buildings_path, engine='pyogrio').to_crs(crs_utm)
    
    pois = gpd.read_file(os.path.join(raw_dir, '04_digitaltwin_pois.geojson.geojson'), engine='pyogrio').to_crs(crs_utm)
    roads = gpd.read_file(os.path.join(raw_dir, '03_digitaltwin_roads.geojson.geojson'), engine='pyogrio').to_crs(crs_utm)
    transit = gpd.read_file(os.path.join(raw_dir, '02_digitaltwin_transit.geojson.geojson'), engine='pyogrio').to_crs(crs_utm)
    
    dem_path = os.path.join(raw_dir, 'chongqingZ_elevation_utm.tif')
    viirs_path = os.path.join(raw_dir, 'chongqingZ_viirs.tif')
    
    print("Extrayendo topografia y luminiscencia nocturna (VIIRS)...")
    buildings['elevation'] = extract_raster_values(buildings, dem_path)
    transit['elevation'] = extract_raster_values(transit, dem_path)
    buildings['val_viirs'] = extract_raster_values(buildings, viirs_path)
    
    # Validacion de seguridad para evitar cargas inutiles
    print(f"DEBUG: Valor maximo de VIIRS detectado: {buildings['val_viirs'].max()}")
    
    print("Calculando distancias equivalentes al transporte...")
    transit_tree = cKDTree(np.array(list(zip(transit.geometry.x, transit.geometry.y))))
    b_coords = np.array(list(zip(buildings.geometry.centroid.x, buildings.geometry.centroid.y)))
    
    dists, indices = transit_tree.query(b_coords)
    network_dists = dists * 1.3 
    
    transit_elevs = transit.iloc[indices]['elevation'].values
    delta_z = np.abs(buildings['elevation'].values - transit_elevs)
    equivalent_dists = network_dists + (delta_z * 10)
    
    buildings['dist_transit_eq'] = equivalent_dists
    
    print("Calculando densidad comercial...")
    poi_tree = cKDTree(np.array(list(zip(pois.geometry.x, pois.geometry.y))))
    poi_counts = poi_tree.query_ball_point(b_coords, r=200)
    buildings['poi_count_200m'] = [len(p) for p in poi_counts]
    
    print("Asignando jerarquia vial...")
    centroids = buildings.geometry.centroid
    nearest_road_indices = roads.sindex.nearest(centroids, return_all=False)[1]
    nearest_road_types = roads.iloc[nearest_road_indices]['highway'].astype(str).str.lower().values
    
    def get_road_weight(rt_str):
        if 'trunk' in rt_str or 'motorway' in rt_str: return 100
        if 'primary' in rt_str: return 85
        if 'secondary' in rt_str: return 60
        if 'tertiary' in rt_str or 'residential' in rt_str: return 30
        return 10

    buildings['road_weight'] = [get_road_weight(rt) for rt in nearest_road_types]
    
    print("Ejecutando inferencia de alturas...")
    max_pois = buildings['poi_count_200m'].max() if buildings['poi_count_200m'].max() > 0 else 1
    
    scores = []
    for _, row in buildings.iterrows():
        t_score = max(0, (800 - row['dist_transit_eq']) / 8) 
        p_score = (row['poi_count_200m'] / max_pois) * 100
        r_score = row['road_weight']
        
        final_score = (t_score * 0.4) + (p_score * 0.3) + (r_score * 0.3)
        scores.append(final_score)
        
    buildings['inference_score'] = scores
    
    print("Consolidando geometria y metricas finales...")
    buildings['area_sqm'] = buildings.geometry.area
    buildings['inferred_levels'] = buildings.apply(lambda x: assign_building_heights(x['area_sqm'], x['inference_score']), axis=1)
    buildings['inferred_height_m'] = buildings['inferred_levels'] * 3.0
    
    print("Preparando datos para exportacion web...")
    cols_to_keep = ['geometry', 'elevation', 'dist_transit_eq', 'poi_count_200m', 
                    'road_weight', 'inference_score', 'area_sqm', 'inferred_levels', 'inferred_height_m', 'val_viirs']
    
    buildings_export = buildings[cols_to_keep]
    buildings_export = buildings_export.explode(index_parts=False)
    buildings_export = buildings_export.to_crs('EPSG:4326')
    
    output_path = os.path.join(processed_dir, 'chongqingZ_inferred_buildings.geojson')
    buildings_export.to_file(output_path, driver='GeoJSON', engine='pyogrio')
    print(f"Proceso finalizado. Archivo consolidado guardado en: {output_path}")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    PROCESSED_DIR = os.path.join(SCRIPT_DIR, '../data/processed')
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    process_inference_model(RAW_DIR, PROCESSED_DIR)