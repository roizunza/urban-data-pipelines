import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

pd.options.mode.string_storage = 'python'
ox.settings.use_cache = True
ox.settings.log_console = True

def _clean_attributes(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Estandariza los tipos de datos en el GeoDataFrame para asegurar 
    la compatibilidad de escritura con pyogrio.
    """
    for col in gdf.columns:
        if col != 'geometry':
            gdf[col] = gdf[col].apply(lambda x: str(x) if isinstance(x, list) else x).astype(str).astype(object)
    return gdf

def extract_transit_nodes(place_query: str, output_dir: str) -> None:
    """
    Extrae representaciones puntuales de estaciones de transporte publico 
    masivo (metro y monorriel) utilizando la API de Overpass.
    """
    print(f"Extrayendo red de transporte masivo para: {place_query}")
    
    tags = {
        'railway': ['station', 'subway_entrance'],
        'station': ['subway', 'monorail']
    }
    
    try:
        transit = ox.features_from_place(place_query, tags=tags)
        
        # Aislar nodos y centroides 
        transit_points = transit[transit.geometry.type == 'Point'].copy()
        
        if transit_points.empty:
            print("Advertencia: No se encontraron nodos puntuales con los tags especificados.")
            return
            
        cols_to_keep = ['geometry', 'name', 'name:en', 'railway', 'station', 'line']
        existing_cols = [col for col in cols_to_keep if col in transit_points.columns]
        transit_points = transit_points[existing_cols]
        
        transit_points = _clean_attributes(transit_points)
        
        output_path = os.path.join(output_dir, 'chongqingZ_transit_nodes.geojson')
        transit_points.to_file(output_path, driver='GeoJSON', engine='pyogrio')
        print(f"Extraccion completada. Nodos guardados en: {output_path}")
        
    except Exception as e:
        print(f"Error critico en la extraccion de transporte: {e}")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DATA_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    
    TARGET_PLACE = "Yuzhong District, Chongqing, China"
    extract_transit_nodes(TARGET_PLACE, RAW_DATA_DIR)