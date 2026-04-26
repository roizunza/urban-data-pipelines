import requests
import json
import os
import time

def extract_boundaries():
    print("Iniciando cacería de fronteras territoriales...")
    
    # Lista de lugares a buscar
    lugares = [
        {"query": "Hong Kong", "nombre": "Hong Kong", "tipo": "Region"},
        {"query": "Shenzhen, China", "nombre": "Shenzhen", "tipo": "Ciudad"},
        {"query": "Nanshan District, Shenzhen", "nombre": "Nanshan", "tipo": "Distrito"},
        {"query": "Futian District, Shenzhen", "nombre": "Futian", "tipo": "Distrito"},
        {"query": "Luohu District, Shenzhen", "nombre": "Luohu", "tipo": "Distrito"},
        {"query": "Bao'an District, Shenzhen", "nombre": "Bao'an", "tipo": "Distrito"},
        {"query": "Longgang District, Shenzhen", "nombre": "Longgang", "tipo": "Distrito"},
        {"query": "Yantian District, Shenzhen", "nombre": "Yantian", "tipo": "Distrito"},
        {"query": "Longhua District, Shenzhen", "nombre": "Longhua", "tipo": "Distrito"},
        {"query": "Pingshan District, Shenzhen", "nombre": "Pingshan", "tipo": "Distrito"},
        {"query": "Guangming District, Shenzhen", "nombre": "Guangming", "tipo": "Distrito"},
        {"query": "Dapeng New District, Shenzhen", "nombre": "Dapeng", "tipo": "Distrito"}
    ]
    
    features = []
    
    # La URL de Nominatim para obtener geometrías
    url = "https://nominatim.openstreetmap.org/search"
    headers = {'User-Agent': 'ShenzhenLogisticsPortfolio/1.0 (Investigacion Academica)'}
    
    for lugar in lugares:
        print(f"Buscando el polígono de: {lugar['nombre']}...")
        params = {
            'q': lugar['query'],
            'format': 'json',
            'polygon_geojson': 1, 
            'limit': 1
        }
        
        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
            data = res.json()
            
            if len(data) > 0 and 'geojson' in data[0]:
                feat = {
                    "type": "Feature",
                    "properties": {
                        "nombre": lugar['nombre'],
                        "tipo": lugar['tipo']
                    },
                    "geometry": data[0]['geojson']
                }
                features.append(feat)
                print(f"  ✓ {lugar['nombre']} capturado.")
            else:
                print(f"  X No se encontró polígono exacto para {lugar['nombre']}")
                
        except Exception as e:
            print(f"  ! Error conectando con {lugar['nombre']}: {e}")
             
        time.sleep(1.5)
        
    geojson_final = {
        "type": "FeatureCollection",
        "features": features
    }
    
    output_path = os.path.join('data', 'processed', 'boundaries_shenzhen_hk.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_final, f, ensure_ascii=False)
        
    print(f"\n¡Extracción finalizada! Archivo guardado en: {output_path}")

if __name__ == "__main__":
    extract_boundaries()