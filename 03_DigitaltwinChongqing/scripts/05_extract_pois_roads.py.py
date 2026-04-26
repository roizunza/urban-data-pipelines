import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

pd.options.mode.string_storage = 'python'
ox.settings.use_cache = True
ox.settings.log_console = True

def _clean_attributes(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Estandariza los tipos de datos en el GeoDataFrame para asegurar la compatibilidad de escritura con pyogrio.
    Convierte los atributos de tipo lista a representaciones de cadena de texto.
    """
    for col in gdf.columns:
        if col != 'geometry':
            gdf[col] = gdf[col].apply(lambda x: str(x) if isinstance(x, list) else x).astype(str).astype(object)
    return gdf

def extract_strategic_pois(place_query: str, output_dir: str) -> None:
    """
    Extrae Puntos de Interés (POIs) basados en el carácter financiero y turístico del distrito de Yuzhong.
    """
    print(f"Extrayendo POIs estratégicos para: {place_query}")
    
    # Etiquetas seleccionadas basadas en el CBD y contexto turístico de Yuzhong
    tags = {
        'office': True,
        'amenity': ['bank', 'marketplace'],
        'tourism': ['hotel', 'museum', 'attraction', 'viewpoint'],
        'shop': ['mall', 'department_store', 'supermarket']
    }
    
    try:
        pois = ox.features_from_place(place_query, tags=tags)
        
        # Aislar centroides para mantener una capa de puntos limpia para el cálculo de distancias
        pois['geometry'] = pois.centroid
        pois_points = pois[pois.geometry.type == 'Point'].copy()
        
        cols_to_keep = ['geometry', 'name', 'amenity', 'tourism', 'shop', 'office']
        existing_cols = [col for col in cols_to_keep if col in pois_points.columns]
        pois_points = pois_points[existing_cols]
        
        pois_points = _clean_attributes(pois_points)
        
        output_path = os.path.join(output_dir, 'chongqingZ_pois.geojson')
        pois_points.to_file(output_path, driver='GeoJSON', engine='pyogrio')
        print(f"Extracción de POIs completada. Archivo guardado en: {output_path}")
        
    except Exception as e:
        print(f"Error crítico durante la extracción de POIs: {e}")

def extract_road_hierarchy(place_query: str, output_dir: str) -> None:
    """
    Extrae la red vial transitable para obtener las etiquetas de jerarquía 'highway',
    las cuales actúan como un proxy para la escala de construcción permitida.
    """
    print(f"Extrayendo jerarquía vial para: {place_query}")
    
    try:
        graph = ox.graph_from_place(place_query, network_type='drive', simplify=True)
        _, edges = ox.graph_to_gdfs(graph)
        
        cols_to_keep = ['geometry', 'highway', 'lanes', 'maxspeed']
        existing_cols = [col for col in cols_to_keep if col in edges.columns]
        edges = edges[existing_cols]
        
        edges = _clean_attributes(edges)
        
        output_path = os.path.join(output_dir, 'chongqingZ_road_hierarchy.geojson')
        edges.to_file(output_path, driver='GeoJSON', engine='pyogrio')
        print(f"Extracción de jerarquía vial completada. Archivo guardado en: {output_path}")
        
    except Exception as e:
        print(f"Error crítico durante la extracción de jerarquía vial: {e}")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DATA_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    
    TARGET_PLACE = "Yuzhong District, Chongqing, China"
    
    extract_strategic_pois(TARGET_PLACE, RAW_DATA_DIR)
    extract_road_hierarchy(TARGET_PLACE, RAW_DATA_DIR)