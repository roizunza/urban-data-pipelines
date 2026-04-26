import os
import subprocess
import geopandas as gpd

def get_bbox_string(filepath: str) -> str:
    """
    Lee el archivo vectorial base y devuelve el bounding box 
    en el formato requerido por Overture Maps (Oeste, Sur, Este, Norte).
    """
    gdf = gpd.read_file(filepath, engine='pyogrio')
    bounds = gdf.total_bounds
    return f"{bounds[0]},{bounds[1]},{bounds[2]},{bounds[3]}"

def extract_overture_buildings(bbox: str, output_path: str) -> None:
    """
    Ejecuta el CLI de overturemaps como subproceso forzando codificacion UTF-8
    para evitar crashes en Windows con caracteres asiaticos.
    """
    print(f"Descargando edificios de Overture Maps para el bbox: {bbox}")
    
    command = [
        "overturemaps", "download",
        "--bbox", bbox,
        "-f", "geojson",
        "--type", "building",
        "-o", output_path
    ]
    
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    
    try:
        subprocess.run(command, check=True, env=env)
        print(f"Extraccion de Overture completada. Archivo guardado en: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error critico al ejecutar el cliente de Overture: {e}")

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DATA_DIR = os.path.join(SCRIPT_DIR, '../data/raw')
    
    NETWORK_PATH = os.path.join(RAW_DATA_DIR, 'chongqingZ_walk_network.geojson')
    OUTPUT_PATH = os.path.join(RAW_DATA_DIR, 'chongqingZ_overture_buildings.geojson')
    
    if not os.path.exists(NETWORK_PATH):
        print("Error: No se encontro el archivo de red peatonal para calcular el area.")
    else:
        bbox_str = get_bbox_string(NETWORK_PATH)
        extract_overture_buildings(bbox_str, OUTPUT_PATH)