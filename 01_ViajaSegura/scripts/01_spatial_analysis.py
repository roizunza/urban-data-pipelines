import pandas as pd
import geopandas as gpd
from pathlib import Path

# Rutas
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
STOPS_PATH = PROJECT_DIR / "data" / "raw" / "paradas_r66.json"
ISOCHRONES_PATH = PROJECT_DIR / "data" / "raw" / "isocronas.json" 
EQUIPAMIENTO_PATH = PROJECT_DIR / "data" / "raw" / "equipamiento.json"
OUTPUT_PATH = PROJECT_DIR / "data" / "processed" / "01_viajasegura_metricas_demanda.geojson"

def run_spatial_analysis():
    print("Cargando paradas e infraestructura real...")
    # Verificar que los archivos existan antes de cargar
    for p in [STOPS_PATH, ISOCHRONES_PATH, EQUIPAMIENTO_PATH]:
        if not p.exists():
            print(f"✘ Error: No se encuentra el archivo en {p}")
            return

    stops_gdf = gpd.read_file(STOPS_PATH)
    iso_gdf = gpd.read_file(ISOCHRONES_PATH)
    fac_gdf = gpd.read_file(EQUIPAMIENTO_PATH)
    
    # Asegurar que tengan CRS (WGS84)
    for gdf in [stops_gdf, iso_gdf, fac_gdf]:
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)

    # Proyectar a UTM para el cruce (Metros)
    iso_utm = iso_gdf.to_crs(epsg=32614)
    fac_utm = fac_gdf.to_crs(epsg=32614)

    print("Realizando join espacial...")
    # Unir puntos de equipamiento con poligonos de isocrona
    # joined contendra la info de la isocrona (origin_id) para cada punto de equipamiento
    joined = gpd.sjoin(fac_utm, iso_utm, how="inner", predicate="intersects")


    print("Realizando join espacial...")
    # Asegurarnos de que el equipamiento tenga un ID único (su índice)
    fac_utm['fac_id'] = fac_utm.index
    
    joined = gpd.sjoin(fac_utm, iso_utm, how="inner", predicate="intersects")
    
    # ELIMINAR DUPLICADOS: Si un equipamiento intersecta múltiples anillos de la misma isócrona, nos quedamos con uno.
    joined = joined.drop_duplicates(subset=['origin_id', 'fac_id'])
    
    # Contar por la columna 'equipamiento'
    equip_counts = joined.groupby(['origin_id', 'equipamiento']).size().unstack(fill_value=0)
    
    # Calcular total de equipamientos por isocrona
    equip_counts['total_equipamientos'] = equip_counts.sum(axis=1)

    # Unir resultados a las paradas originales (fid es la llave en paradas_r66.json)
    print("Integrando conteos a las paradas...")
    final_gdf = stops_gdf.merge(equip_counts, left_on='fid', right_index=True, how='left')
    
    # Llenar con 0 si una parada no tuvo ningun equipamiento cerca
    final_gdf.fillna(0, inplace=True)
    
    # Score de carga (Inversamente proporcional al equipamiento)
    final_gdf['scorecarga'] = final_gdf['total'] / (final_gdf['total_equipamientos'] + 1)

    print("Guardando GeoJSON final...")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    final_gdf.to_file(OUTPUT_PATH, driver="GeoJSON")
    print(f"✅ ¡Listo! Archivo generado en: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_spatial_analysis()