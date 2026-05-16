import os
import geopandas as gpd

def fix_local_files():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proc_dir = os.path.join(base_dir, "data", "processed")

    archivos = {
        "kamakura_edges.geojson": "kamakura_edges_wgs84.geojson",
        "kamakura_emergent_temples.geojson": "kamakura_temples_wgs84.geojson"
    }

    for in_name, out_name in archivos.items():
        in_path = os.path.join(proc_dir, in_name)
        out_path = os.path.join(proc_dir, out_name)

        if os.path.exists(in_path):
            gdf = gpd.read_file(in_path)
            
            # Forzamos la proyeccion metrica antes de pasar a grados
            if gdf.crs is None:
                gdf.set_crs(epsg=32654, inplace=True)
                
            gdf = gdf.to_crs(epsg=4326)
            gdf.to_file(out_path, driver="GeoJSON")
            print(f"Convertido exitosamente: {out_name}")

if __name__ == "__main__":
    fix_local_files()