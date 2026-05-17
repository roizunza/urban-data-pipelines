import os
import osmnx as ox
import geopandas as gpd

def download_kamakura_baseline():
    print("Iniciando Fase 1: Extraccion de infraestructura base...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)

    place_query = "Kamakura, Kanagawa, Japan"

    # 1. Descarga y desestructuracion de la red vial de OpenStreetMap
    print("Descargando red vial peatonales de Kamakura...")
    graph = ox.graph_from_place(place_query, network_type="walk")
    
    nodes, edges = ox.graph_to_gdfs(graph)
    
    # Estandarizacion de indices para conservar topologia pura
    nodes = nodes.reset_index()
    edges = edges.reset_index()

    # 2. Descarga de refugios gubernamentales oficiales
    print("Extrayendo refugios oficiales de evacuacion...")
    shelters_tags = {"amenity": ["public_building", "school", "townhall"]}
    shelters_gdf = ox.geometries_from_place(place_query, tags=shelters_tags)
    shelters_gdf = shelters_gdf[shelters_gdf.geometry.type == 'Point']

    # 3. Descarga de la red de templos y lugares de culto (Infraestructura latente)
    print("Extrayendo red de templos y santuarios historicos...")
    temples_tags = {"amenity": "place_of_worship", "religion": ["buddhist", "shinto"]}
    temples_gdf = ox.geometries_from_place(place_query, tags=temples_tags)

    # Exportacion limpia a GeoJSON en formato metrico local (UTM Zona 54N)
    print("Normalizando proyecciones espaciales a EPSG:32654...")
    
    nodes = nodes.to_crs(epsg=32654)
    edges = edges.to_crs(epsg=32654)
    shelters_gdf = shelters_gdf.to_crs(epsg=32654)
    temples_gdf = temples_gdf.to_crs(epsg=32654)

    nodes.to_file(os.path.join(output_dir, "kamakura_nodes.geojson"), driver="GeoJSON")
    edges.to_file(os.path.join(output_dir, "kamakura_edges.geojson"), driver="GeoJSON")
    shelters_gdf.to_file(os.path.join(output_dir, "kamakura_official_shelters.geojson"), driver="GeoJSON")
    temples_gdf.to_file(os.path.join(output_dir, "kamakura_emergent_temples.geojson"), driver="GeoJSON")

    print("\n[Exito] Archivos de infraestructura base almacenados en data/processed/")

if __name__ == "__main__":
    download_kamakura_baseline()