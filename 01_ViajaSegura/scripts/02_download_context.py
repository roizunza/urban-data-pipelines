import osmnx as ox
from pathlib import Path

# Rutas 
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# CORRECCIÓN: Bounding box (Oeste, Sur, Este, Norte)
bbox = (-99.280, 19.290, -99.170, 19.355)

print("Descargando contorno de Ciudad Universitaria...")
cu = ox.features_from_bbox(bbox=bbox, tags={'name': 'Ciudad Universitaria'})
cu.to_file(RAW_DIR / "cu_polygon.json", driver="GeoJSON")

print("Descargando vías de acceso controlado (Periférico)...")
peri = ox.features_from_bbox(bbox=bbox, tags={'highway': ['motorway', 'trunk']})
peri.to_file(RAW_DIR / "periferico.json", driver="GeoJSON")

print("Descargando punto del Metro Miguel Ángel de Quevedo...")
maq = ox.features_from_bbox(bbox=bbox, tags={'railway': 'station', 'name': 'Miguel Ángel de Quevedo'})
maq.to_file(RAW_DIR / "metro_maq.json", driver="GeoJSON")

print(f"¡Listo! Archivos crudos guardados correctamente en: {RAW_DIR}")