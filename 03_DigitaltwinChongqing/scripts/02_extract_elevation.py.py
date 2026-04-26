import os
import ee
import requests
import zipfile
import io
import geopandas as gpd

def get_aoi_from_network(filepath: str) -> ee.Geometry:
    """Lee el GeoJSON de las calles y extrae la caja envolvente (bounding box) para el DEM."""
    print("Leyendo extension espacial de la red peatonal...")
    gdf = gpd.read_file(filepath, engine='pyogrio')
    bounds = gdf.total_bounds # [minx, miny, maxx, maxy]
    
    # Crear un rectangulo en Earth Engine usando coordenadas locales
    aoi = ee.Geometry.Rectangle([bounds[0], bounds[1], bounds[2], bounds[3]])
    return aoi

def extract_dem(aoi: ee.Geometry, output_dir: str) -> None:
    """Descarga el DEM SRTM de 30m recortado y proyectado a UTM."""
    print("Conectando con los servidores de Google Earth Engine...")
    
    # SRTM de 30 metros de resolucion global de la NASA
    dem = ee.Image('USGS/SRTMGL1_003')
    
    # Recortar al area 
    dem_clipped = dem.clip(aoi)
    
    # Chongqing esta en la zona UTM 48N (EPSG:32648)
    utm_crs = 'EPSG:32648'
    print(f"Solicitando el modelo de elevacion proyectado a {utm_crs}...")
    
    url = dem_clipped.getDownloadURL({
        'scale': 30,
        'crs': utm_crs,
        'region': aoi,
        'format': 'GEO_TIFF'
    })
    
    print("Descargando la informacion topografica...")
    response = requests.get(url)
    
    if response.status_code == 200:
        output_path = os.path.join(output_dir, 'chongqingZ_elevation_utm.tif')
        
        file_signature = response.content[:2]
        
        if file_signature == b'PK':  
            print("Google envio un archivo comprimido. Extrayendo .tif...")
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                tif_name = [name for name in z.namelist() if name.endswith('.tif')][0]
                with open(output_path, 'wb') as f:
                    f.write(z.read(tif_name))
            print(f"Extraccion del Eje Z completada. DEM guardado en: {output_path}")
            
        elif file_signature in (b'II', b'MM'):  
            print("Google envio el .tif directo. Guardando...")
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Extraccion del Eje Z completada. DEM guardado en: {output_path}")
            
        else:
            print("Earth Engine devolvio un formato inesperado o un mensaje de error:")
            print(response.content[:500])
    else:
        print(f"Error en la descarga: codigo {response.status_code}")
        print(response.text)
        
if __name__ == "__main__":
    # Autenticacion local
    try:
        ee.Initialize()
    except Exception as e:
        print("Iniciando flujo de autenticacion de Earth Engine...")
        ee.Authenticate()
        ee.Initialize()
        
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DATA_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    NETWORK_PATH = os.path.join(RAW_DATA_DIR, 'chongqingZ_walk_network.geojson')
    
    if not os.path.exists(NETWORK_PATH):
        print("Error: No se encontro el archivo de calles. Corre el script de OSM primero.")
    else:
        aoi_geometry = get_aoi_from_network(NETWORK_PATH)
        extract_dem(aoi_geometry, RAW_DATA_DIR)