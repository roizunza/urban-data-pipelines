import os
import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio

pd.options.mode.string_storage = 'python'

def extract_raster_value(coords: list, raster_path: str) -> np.ndarray:
    """Extrae valores de un raster para una lista de coordenadas WGS84."""
    values = []
    try:
        with rasterio.open(raster_path) as src:
            for val in src.sample(coords):
                values.append(val[0])
    except Exception as e:
        print(f"Error de lectura en raster: {e}")
        return np.zeros(len(coords))
    return np.array(values)

def validate_digital_twin(processed_dir: str, raw_dir: str) -> None:
    print("Iniciando validacion del modelo espacial...")
    
    buildings_path = os.path.join(processed_dir, 'chongqingZ_inferred_buildings.geojson')
    buildings = gpd.read_file(buildings_path, engine='pyogrio')
    
    # 1. Calcular centroides en el CRS original (UTM / metros) para evitar distorsiones
    centroids = buildings.geometry.centroid
    
    # 2. Proyectar solo esos puntos a WGS84 para poder leer los rasters satelitales
    centroids_wgs84 = gpd.GeoSeries(centroids, crs=buildings.crs).to_crs("EPSG:4326")
    coords = [(geom.x, geom.y) for geom in centroids_wgs84]
    
    print("Extrayendo validadores fisicos...")
    viirs_path = os.path.join(raw_dir, 'chongqingZ_viirs.tif')
    
    buildings['val_viirs'] = extract_raster_value(coords, viirs_path)
    
    # Limpieza de anomalias en bordes de raster
    buildings['val_viirs'] = np.where(buildings['val_viirs'] < 0, 0, buildings['val_viirs'])
    
    # Exportar GeoJSON final
    output_path = os.path.join(processed_dir, 'chongqingZ_digital_twin_validated.geojson')
    buildings.to_file(output_path, driver='GeoJSON', engine='pyogrio')
    
    # Reporte Estadistico de Validacion (Por Deciles)
    print("\n" + "="*40)
    print(" REPORTE DE GROUND-TRUTHING (VALIDACION)")
    print("="*40)
    
    # Segmentacion por deciles (Top 10% mas altos vs Bottom 10% mas bajos)
    umbral_alto = buildings['inferred_levels'].quantile(0.90)
    umbral_bajo = buildings['inferred_levels'].quantile(0.10)
    
    alta_densidad = buildings[buildings['inferred_levels'] >= umbral_alto]
    baja_densidad = buildings[buildings['inferred_levels'] <= umbral_bajo]
    
    print(f"Segmentando {len(alta_densidad)} edificios de alta densidad vs {len(baja_densidad)} de baja densidad.\n")
    
    print(f"1. CORRELACION LUMINICA (Actividad Economica VIIRS):")
    print(f"   -> Top 10% (Rascacielos/Alta Densidad): Promedio Rad: {alta_densidad['val_viirs'].mean():.2f}")
    print(f"   -> Bottom 10% (Baja Densidad):          Promedio Rad: {baja_densidad['val_viirs'].mean():.2f}")
    print(f"   * Exito: El valor del Top 10% debe ser mayor al Bottom 10%.\n")
    print("="*40 + "\n")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    PROCESSED_DIR = os.path.join(SCRIPT_DIR, '../data/processed')
    validate_digital_twin(PROCESSED_DIR, RAW_DIR)