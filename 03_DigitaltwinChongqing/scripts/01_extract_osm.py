import os
import osmnx as ox
import geopandas as gpd
import pandas as pd

pd.options.mode.string_storage = 'python'

# Configuracion global de osmnx
ox.settings.use_cache = True
ox.settings.log_console = True

def create_directory_structure(base_path: str) -> None:
    """Crea la estructura de carpetas para el almacenamiento de datos brutos y procesados."""
    directories = ['../data/raw', '../data/processed']
    for directory in directories:
        os.makedirs(os.path.join(base_path, directory), exist_ok=True)

def _clean_attributes(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Limpieza extrema de atributos. Convierte listas a strings y fuerza 
    el tipo object de Python para evadir conflictos en los motores OGR.
    """
    for col in gdf.columns:
        if col != 'geometry':
            gdf[col] = gdf[col].apply(lambda x: str(x) if isinstance(x, list) else x).astype(str).astype(object)
    return gdf

def extract_urban_features(place_query: str, output_dir: str) -> None:
    """
    Extrae la red peatonal y las geometrias de construccion desde la API de Overpass.
    Exporta los datos en formato GeoJSON utilizando pyogrio.
    """
    try:
        # 1. Extraccion de la red de movilidad (peatonal)
        print(f"Extrayendo red peatonal para: {place_query}")
        graph = ox.graph_from_place(place_query, network_type='walk', simplify=True)
        nodes, edges = ox.graph_to_gdfs(graph)
        
        edges = _clean_attributes(edges)
        walk_path = os.path.join(output_dir, 'chongqingZ_walk_network.geojson')
        edges.to_file(walk_path, driver='GeoJSON', engine='pyogrio')
        
        # 2. Extraccion de huellas arquitectonicas (edificios)
        print(f"Extrayendo huellas de edificios para: {place_query}")
        tags = {'building': True}
        buildings = ox.features_from_place(place_query, tags=tags)
        
        # Filtrado de geometrias invalidas
        buildings = buildings[buildings.geometry.type.isin(['Polygon', 'MultiPolygon'])]
        
        # Seleccion de columnas minimas
        cols_to_keep = ['geometry', 'building', 'building:levels', 'height']
        existing_cols = [col for col in cols_to_keep if col in buildings.columns]
        buildings = buildings[existing_cols]
        
        buildings = _clean_attributes(buildings)
        buildings_path = os.path.join(output_dir, 'chongqingZ_buildings.geojson')
        buildings.to_file(buildings_path, driver='GeoJSON', engine='pyogrio')
        
        print("Extraccion completada con exito. Archivos GeoJSON generados.")
        
    except Exception as e:
        print(f"Error critico en la extraccion espacial: {e}")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DATA_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    
    create_directory_structure(SCRIPT_DIR)
    
    TARGET_PLACE = "Yuzhong District, Chongqing, China"
    extract_urban_features(TARGET_PLACE, RAW_DATA_DIR)