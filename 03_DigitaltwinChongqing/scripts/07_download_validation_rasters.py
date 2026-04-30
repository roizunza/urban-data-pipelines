import os
import ee
import requests
import geopandas as gpd

def initialize_ee() -> None:
    try:
        ee.Initialize()
    except Exception:
        print("Autenticacion requerida. Ejecuta 'earthengine authenticate' en la terminal.")
        ee.Authenticate()
        ee.Initialize()

def download_validation_rasters(processed_dir: str, raw_dir: str) -> None:
    print("Iniciando descarga de imagenes satelitales (GEE)...")
    
    # Extraer Bounding Box en WGS84
    grid_path = os.path.join(processed_dir, 'chongqingZ_hex_grid.geojson')
    grid = gpd.read_file(grid_path, engine='pyogrio')
    grid_wgs84 = grid.to_crs("EPSG:4326")
    minx, miny, maxx, maxy = grid_wgs84.total_bounds
    
    roi = ee.Geometry.Rectangle([minx, miny, maxx, maxy])
    
    # 1. VIIRS Nighttime Lights (Promedio anual reciente)
    print("Procesando satelite Suomi NPP (VIIRS)...")
    viirs = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG") \
        .filterDate('2023-01-01', '2023-12-31') \
        .select('avg_rad') \
        .median() \
        .clip(roi)
    
    def download_ee_image(image: ee.Image, filename: str, scale: int) -> None:
        try:
            url = image.getDownloadURL({
                'scale': scale,
                'crs': 'EPSG:4326',
                'region': roi,
                'format': 'GEO_TIFF'  
            })
            response = requests.get(url)
            filepath = os.path.join(raw_dir, filename)
            with open(filepath, 'wb') as fd:
                fd.write(response.content)
            print(f"Raster descargado con exito: {filepath}")
        except Exception as e:
            print(f"Error descargando {filename}: {e}")

    # Descargas (VIIRS a 100m)
    download_ee_image(viirs, 'chongqingZ_viirs.tif', 100)

if __name__ == "__main__":
    initialize_ee()
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    PROCESSED_DIR = os.path.join(SCRIPT_DIR, '../data/processed')
    download_validation_rasters(PROCESSED_DIR, RAW_DIR)