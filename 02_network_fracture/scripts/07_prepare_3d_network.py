import os
import geopandas as gpd

def prepare_3d_network():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    in_path = os.path.join(base_dir, "data", "processed", "kamakura_edges_3d.geojson")
    out_path = os.path.join(base_dir, "data", "processed", "kamakura_edges_3d_wgs84.geojson")

    print("Procesando red vial topografica...")
    gdf = gpd.read_file(in_path)
    
    if gdf.crs is None or gdf.crs.to_epsg() != 32654:
        gdf.set_crs(epsg=32654, inplace=True, allow_override=True)
        
    gdf = gdf.to_crs(epsg=4326)
    
    # Mantener solo columnas esenciales para optimizar rendimiento web
    columnas = ['u', 'v', 'highway', 'min_elevation', 'geometry']
    gdf_limpio = gdf[columnas]
    
    gdf_limpio.to_file(out_path, driver="GeoJSON")
    print(f"Red lista para la web en: {out_path}")

if __name__ == "__main__":
    prepare_3d_network()