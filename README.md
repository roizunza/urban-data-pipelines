# Detección de Cuellos de Botella en Infraestructura EV: El Caso Logístico de Shenzhen

## 1. El propósito del análisis realizado
Shenzhen es la primera megaciudad del mundo en electrificar casi por completo su flota de transporte y logística. Sin embargo, la transición energética presenta retos de equidad espacial. 

El propósito de este proyecto de Ingeniería de Datos Espaciales es identificar "desiertos de carga eléctrica" para el sector comercial. Mediante el uso de inteligencia artificial (DBSCAN), se detectaron clústeres de altísima demanda logística (centros de mensajería y distribución hiperdensos) para luego cruzar su ubicación geométrica con la red de cargadores eléctricos disponibles, detectando cuellos de botella operativos donde la demanda supera con creces la oferta de infraestructura.

## 2. La estructura del proyecto y organización de los archivos
El pipeline se construyó utilizando Python para la extracción y modelado, organizado con una base de datos PostgreSQL/PostGIS alojada en Supabase para el procesamiento espacial.

```text
/03_logistica_ev_shenzhen
├── data/
│   ├── raw/                 # Archivos JSON crudos extraídos de la API (Overpass)
│   └── processed/           # Resultados en formato GeoJSON listos para visualización web
├── scripts/
│   ├── 01_extract_data.py   # Script de Web Scraping/API request con headers seguros
│   ├── 02_load_postgis.py   # Conexión psycopg2, creación de esquema relacional y carga espacial
│   └── 03_ml_clustering.py  # Modelo DBSCAN y cruce geométrico (sjoin) con scikit-learn y GeoPandas
├── .env                     # Credenciales de conexión a Supabase (ignorado en Git)
└── README.md                # Documentación del pipeline
```

## 3. Ejemplos de gráficos e insights obtenidos
A través de la aplicación de Machine Learning Espacial (DBSCAN con un radio de 500m y densidad mínima de 3 nodos), el algoritmo logró agrupar la demanda bruta, revelando una deficiencia crítica en la planeación urbana:

* **Insight Principal:** Se identificaron **8 macro-clústeres** de altísima demanda logística.
* **Falla de Infraestructura:** El análisis de proximidad geométrica reveló que **7 de los 8 clústeres** se encuentran en estado de **Riesgo Crítico**, al no tener ninguna estación de carga eléctrica a menos de 1 kilómetro a la redonda (algunos teniendo que desplazarse hasta 8 kilómetros para cargar).
* **Conclusión Comercial:** La infraestructura de carga de Shenzhen parece estar orientada a vehículos particulares de consumo (zonas residenciales/comerciales), abandonando la operatividad de las flotillas de última milla.

## 4. Instrucciones para ejecutar el pipeline
Para reproducir este análisis en tu máquina local:

1. Clona el repositorio e ingresa a la carpeta del proyecto.
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate
   pip install pandas geopandas sqlalchemy psycopg2-binary requests python-dotenv scikit-learn shapely
   ```
3. Configura tu base de datos PostgreSQL con PostGIS habilitado y crea un archivo `.env` en la raíz con tus credenciales: `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`.
4. Ejecuta los scripts en orden secuencial:
   ```bash
   python scripts/01_extract_data.py
   python scripts/02_load_postgis.py
   python scripts/03_ml_clustering.py
   ```
5. El resultado final se guardará en `data/processed/cuellos_de_botella.geojson`.
```