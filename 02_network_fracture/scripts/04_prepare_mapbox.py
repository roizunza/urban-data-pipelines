import os
import geopandas as gpd

def clean_for_mapbox():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    in_path = os.path.join(base_dir, "data", "processed", "kamakura_nodes_simulated.geojson")
    out_path = os.path.join(base_dir, "data", "processed", "kamakura_mapbox_ready.geojson")

    print("Cargando archivo simulado completo...")
    gdf = gpd.read_file(in_path)

    columnas_esenciales = [
        'orphan_off_0m', 'saved_by_temple_0m',
        'orphan_off_10m', 'saved_by_temple_10m',
        'orphan_off_20m', 'saved_by_temple_20m',
        'orphan_off_30m', 'saved_by_temple_30m',
        'geometry'
    ]

    print("Filtrando atributos y transformando a WGS84 (Lat/Lon)...")
    gdf_clean = gdf[columnas_esenciales].copy()
    
    # EL PARCHE: Regresamos las coordenadas a Latitud/Longitud para Mapbox
    gdf_clean = gdf_clean.to_crs("EPSG:4326")

    print("Exportando archivo ligero para la nube...")
    gdf_clean.to_file(out_path, driver="GeoJSON")
    print(f"[Exito] Archivo listo para Mapbox en: {out_path}")

if __name__ == "__main__":
    clean_for_mapbox()