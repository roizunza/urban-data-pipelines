import os
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import DBSCAN
from dotenv import load_dotenv

load_dotenv()

def run_spatial_clustering():
    """
    Extrae los datos de Supabase, ejecuta un algoritmo DBSCAN para encontrar
    clústeres de alta demanda logística y calcula la distancia al cargador más cercano
    para detectar cuellos de botella (zonas rojas).
    """
    
    # 1. Conexión a la base de datos mediante SQLAlchemy para GeoPandas
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
    
    print("Extrayendo datos desde Supabase...")
    
    # Extracción usando PostGIS directamente a un GeoDataFrame
    gdf_nodos = gpd.read_postgis("SELECT * FROM nodos_logistica", con=engine, geom_col='geom')
    gdf_cargadores = gpd.read_postgis("SELECT * FROM cargadores_ev", con=engine, geom_col='geom')
    
    # 2. Proyección Espacial
    # Conversión de grados (EPSG:4326) a metros (EPSG:32650, UTM Zona 50N para Shenzhen)
    # Importantísimo para que el algoritmo de ML mida en metros reales
    gdf_nodos = gdf_nodos.to_crs(epsg=32650)
    gdf_cargadores = gdf_cargadores.to_crs(epsg=32650)
    
    print("Ejecutando algoritmo DBSCAN de Machine Learning...")
    
    # 3. Algoritmo DBSCAN
    # Parámetros: eps=500 (metros de radio), min_samples=3 (mínimo de nodos para ser clúster)
    coordenadas = pd.DataFrame({'x': gdf_nodos.geometry.x, 'y': gdf_nodos.geometry.y})
    modelo = DBSCAN(eps=500, min_samples=3)
    gdf_nodos['cluster_id'] = modelo.fit_predict(coordenadas)
    
    # Filtración del ruido (DBSCAN asigna -1 a los puntos que no forman clúster)
    clusters_validos = gdf_nodos[gdf_nodos['cluster_id'] != -1]
    
    if clusters_validos.empty:
        print("No se encontraron clústeres de alta densidad con los parámetros actuales.")
        return

    # 4. Análisis de Cuellos de Botella
    print("Calculando distancias a infraestructura de carga...")
    
    # Calcula el centroide de cada clúster de demanda
    centroides = clusters_validos.dissolve(by='cluster_id').centroid
    gdf_centroides = gpd.GeoDataFrame(geometry=centroides, crs=32650)
    
    # Calcula la distancia desde cada centroide al cargador más cercano
    # Join espacial de cercanía (sjoin_nearest)
    cuellos_botella = gpd.sjoin_nearest(
        gdf_centroides, 
        gdf_cargadores, 
        how='left', 
        distance_col='distancia_a_cargador_m'
    )
    
    # Determinación del nivel de riesgo
    # Si el cargador más cercano está a más de 1000 metros (1 km), es una Zona Roja
    cuellos_botella['nivel_riesgo'] = cuellos_botella['distancia_a_cargador_m'].apply(
        lambda d: 'Riesgo Crítico' if d > 1000 else 'Riesgo Moderado' if d > 500 else 'Cobertura Adecuada'
    )
    
    # 5. Exportar resultados para el portafolio 
    # Latitud/longitud para mapas web
    cuellos_botella = cuellos_botella.to_crs(epsg=4326)
    
    output_path = os.path.join('data', 'processed', 'cuellos_de_botella.geojson')
    cuellos_botella.to_file(output_path, driver='GeoJSON')
    
    print(f"¡Análisis ML completado! Resultados exportados a: {output_path}")
    print("\nResumen de Clústeres de Demanda:")
    print(cuellos_botella[['distancia_a_cargador_m', 'nivel_riesgo']])

if __name__ == "__main__":
    run_spatial_clustering()