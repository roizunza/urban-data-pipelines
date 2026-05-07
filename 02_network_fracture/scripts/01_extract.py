import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.extraction import KamakuraExtractor

def main():
    print("Iniciando Fase 1: Extraccion de Datos para Kamakura...")
    
    # NUEVO ORDEN OSMnx 2.0+: (West, South, East, North)
    bbox_kamakura = (139.5250, 35.2950, 139.5700, 35.3350)
    extractor = KamakuraExtractor(*bbox_kamakura)
    
    print("2. Extrayendo malla vial peatonal...")
    G_walk = extractor.extract_pedestrian_network()
    
    print("3. Extrayendo Infraestructura Oficial (Escuelas y Centros Comunitarios)...")
    tags_official = {'amenity': ['school', 'community_centre', 'public_building']}
    gdf_official = extractor.extract_infrastructure(tags_official)
    
    print("4. Extrayendo Infraestructura Emergente (Templos)...")
    tags_emergent = {'amenity': 'place_of_worship', 'religion': ['buddhist', 'shinto']}
    gdf_emergent = extractor.extract_infrastructure(tags_emergent)
    
    print("5. Exportando capas a GeoJSON...")
    extractor.export_to_geojson(G_walk, gdf_official, gdf_emergent)
    
    print("\n[Exito] Fase 1 completada.")

if __name__ == "__main__":
    main()