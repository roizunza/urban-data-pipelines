import os
import geopandas as gpd

def export_web_pipeline():
    print("Iniciando Pipeline de Exportación Web (Mapbox GL JS)...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proc_dir = os.path.join(base_dir, "data", "processed")

    # Diccionario de archivos a procesar: {Archivo_Entrada: (Archivo_Salida, Columnas_a_conservar)}
    archivos = {
        "kamakura_nodes_simulated.geojson": (
            "kamakura_mapbox_ready.geojson", 
            ['orphan_off_0m', 'saved_by_temple_0m', 'orphan_off_10m', 'saved_by_temple_10m', 'orphan_off_20m', 'saved_by_temple_20m', 'orphan_off_30m', 'saved_by_temple_30m', 'geometry']
        ),
        "kamakura_edges_3d.geojson": (
            "kamakura_edges_3d_wgs84.geojson", 
            ['u', 'v', 'highway', 'min_elevation', 'geometry']
        ),
        "kamakura_emergent_temples.geojson": (
            "kamakura_temples_wgs84.geojson", 
            None # Conservar todas
        )
    }

    for in_name, (out_name, columnas) in archivos.items():
        in_path = os.path.join(proc_dir, in_name)
        out_path = os.path.join(proc_dir, out_name)

        if os.path.exists(in_path):
            print(f"Procesando: {in_name}...")
            gdf = gpd.read_file(in_path)
            
            # Forzar UTM si no lo tiene, luego pasar a WGS84 para la web
            if gdf.crs is None or gdf.crs.to_epsg() != 32654:
                gdf.set_crs(epsg=32654, inplace=True, allow_override=True)
            gdf = gdf.to_crs(epsg=4326)
            
            # Filtrar columnas si se especificó
            if columnas:
                columnas_existentes = [col for col in columnas if col in gdf.columns]
                gdf = gdf[columnas_existentes]

            gdf.to_file(out_path, driver="GeoJSON")
            print(f" -> Exportado con éxito: {out_name}")
        else:
            print(f"[Advertencia] No se encontró el archivo: {in_path}")

if __name__ == "__main__":
    export_web_pipeline()