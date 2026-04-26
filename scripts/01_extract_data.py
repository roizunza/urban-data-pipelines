import requests
import json
import os

def extract_shenzhen_data():
    """
    Consulta la API de Overpass para extraer estaciones de carga y nodos 
    logísticos en el área de Shenzhen, China.
    """
    
    query = """
    [out:json][timeout:90];
    area["name:en"="Shenzhen"]->.searchArea;
    (
      node["amenity"="charging_station"](area.searchArea);
      node["amenity"="post_office"](area.searchArea);
      node["industrial"="logistics"](area.searchArea);
    );
    out body;
    >;
    out skel qt;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    
    # La credencial de acceso para evitar el error 406
    headers = {
        'User-Agent': 'ShenzhenEVLogisticsPortfolio/1.0 (Investigacion Academica)'
    }
    
    print("Iniciando descarga de datos desde OpenStreetMap wait for it...")
    
    try:
        # Inyectamos los headers en la petición
        response = requests.post(url, data={'data': query}, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        output_path = os.path.join('data', 'raw', 'shenzhen_raw_data.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"¡Lo logré!!! la data se guardó en: {output_path}")
        print(f"Se encontraron {len(data['elements'])} elementos.")
        
    except Exception as e:
        print(f"Error en la extracción: {e}")

if __name__ == "__main__":
    extract_shenzhen_data()