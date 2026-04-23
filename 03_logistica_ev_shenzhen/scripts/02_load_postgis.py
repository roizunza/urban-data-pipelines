import json
import os
import psycopg2
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def load_data_to_postgis():
    """
    Lee el archivo JSON local, crea el esquema de base de datos relacional 
    y ejecuta comandos INSERT espaciales hacia PostgreSQL/PostGIS.
    """
    
    # 1. Configuración de conexión usando las variables seguras
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
    except Exception as e:
        print(f"Error crítico al conectar con la base de datos: {e}")
        return

    # 2. Creación de la arquitectura de tablas en SQL
    print("Construyendo arquitectura de tablas en Supabase...")
    
    creacion_tablas_sql = """
        -- Tabla 1: Estaciones de carga para vehículos eléctricos
        DROP TABLE IF EXISTS cargadores_ev;
        CREATE TABLE cargadores_ev (
            id BIGINT PRIMARY KEY,
            nombre VARCHAR(255),
            operador VARCHAR(255),
            geom GEOMETRY(Point, 4326)
        );

        -- Tabla 2: Nodos de distribución y mensajería
        DROP TABLE IF EXISTS nodos_logistica;
        CREATE TABLE nodos_logistica (
            id BIGINT PRIMARY KEY,
            nombre VARCHAR(255),
            marca VARCHAR(255),
            tipo VARCHAR(50),
            geom GEOMETRY(Point, 4326)
        );
    """
    cur.execute(creacion_tablas_sql)
    conn.commit()

    # 3. Lectura del archivo crudo
    file_path = os.path.join('data', 'raw', 'shenzhen_raw_data.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 4. Inyección de datos (Transformación al vuelo)
    print("Limpiando e inyectando datos espaciales...")
    cargadores_count = 0
    nodos_count = 0

    for element in data.get('elements', []):
        if element['type'] == 'node' and 'tags' in element:
            osm_id = element['id']
            lon = element['lon']
            lat = element['lat']
            tags = element['tags']
            
            # Priorizamos el nombre chino, si no hay, buscamos el inglés
            nombre = tags.get('name:zh', tags.get('name', tags.get('name:en', 'Desconocido')))

            # Clasificación y carga para la Tabla 1 (Cargadores)
            if tags.get('amenity') == 'charging_station':
                operador = tags.get('operator', tags.get('brand', 'Independiente'))
                cur.execute("""
                    INSERT INTO cargadores_ev (id, nombre, operador, geom)
                    VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                """, (osm_id, nombre, operador, lon, lat))
                cargadores_count += 1

            # Clasificación y carga para la Tabla 2 (Logística)
            elif tags.get('amenity') == 'post_office' or tags.get('industrial') == 'logistics':
                marca = tags.get('brand', tags.get('network', 'Independiente'))
                tipo = tags.get('amenity', 'Logistics Node')
                cur.execute("""
                    INSERT INTO nodos_logistica (id, nombre, marca, tipo, geom)
                    VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                """, (osm_id, nombre, marca, tipo, lon, lat))
                nodos_count += 1

    # Guardar todos los INSERTS en la base de datos y cerrar la puerta
    conn.commit()
    cur.close()
    conn.close()

    print(f"¡Carga completada exitosamente!")
    print(f"- {cargadores_count} cargadores EV registrados.")
    print(f"- {nodos_count} nodos logísticos registrados.")

if __name__ == "__main__":
    load_data_to_postgis()