# Gemelo Digital 2.5D: Inferencia Espacial en Chongqing

## 1. El Propósito del Análisis Realizado
El objetivo principal de este proyecto es desarrollar una herramienta de geointeligencia denominada **Urban Inference Engine**, capaz de modelar la escala de construcción latente de una ciudad mediante la inferencia de edificabilidad a partir de variables urbanas y territoriales. 

El caso de estudio es la península del distrito de Yuzhong en **Chongqing, China**. La elección de este sitio representa uno de los entornos urbanos más complejos del mundo debido a cinco características fundamentales:
1. **Topografía extrema:** Cambios de elevación abruptos que desafían la cuadrícula urbana tradicional.
2. **Restricción geográfica:** Limitación de expansión física al estar encapsulada por la convergencia de los ríos Yangtze y Jialing.
3. **Densidad hiperconcentrada:** La falta de suelo plano obliga a una ocupación vertical masiva.
4. **Trama vial tridimensional:** Infraestructura adaptada a las laderas que desdibuja la noción tradicional de "planta baja".
5. **Transporte multinivel:** Sistemas de monorraíl que navegan el relieve, cruzando e incluso atravesando edificaciones.

Metodología. 
Para calcular la edificabilidad de más de 16,000 polígonos, el *Urban Inference Engine* ejecuta el siguiente flujo lógico:
- **Toma la huella individual** de cada edificio descargado de Overture Maps.
- **Calcula el área específica** de ese polígono en metros cuadrados (`area_sqm`).
- **Evalúa el contexto:** qué tan cerca está ese polígono exacto del monorraíl (con penalización topográfica), qué calle lo alimenta y cuántos comercios tiene en un radio de 200 metros.
- **Decide los pisos y extruye** ese polígono individual en un modelo 2.5D.

*(Para conocer a profundidad las teorías de Economía Espacial, Sintaxis Espacial y Evaluación Multicriterio que justifican matemáticamente este motor, consulta el [Marco Teórico](./docs/marco_teorico.md)).*

## 2. Estructura del Proyecto y Organización de los Archivos
El repositorio separa la extracción de datos crudos de los vectores procesados que alimentan el frontend (Supabase / Deck.gl).

03_DigitaltwinChongqing/
│
├── cache/                            # Archivos de caché del entorno
│
├── data/
│   ├── raw/                          # Archivos crudos (Ignorados en Git)
│   │   ├── 02_digitaltwin_transit.geojson # Nodos de transporte 
│   │   ├── 03_digitaltwin_roads.geojson   # Jerarquía vial 
│   │   ├── 04_digitaltwin_pois.geojson   # Anclas comerciales
│   │   ├── chongqingZ_buildings.geojson           # Huellas de edificios sin procesar
│   │   └── chongqingZ_walk_network.geojson        # Red peatonal para ruteo topográfico
│   │
│   └── processed/                    # Vectores inferidos (Conexión a React/Supabase)
│       └── chongqingZ_inferred_buildings.geojson  # Huellas con alturas inferidas
│
├── docs/
│   ├── glosario.md                   # Definiciones de términos técnicos espaciales
│   └── marco_teorico.md              # Fundamentos académicos y fórmulas del modelo
│
├── scripts/                          # Pipeline ETL y Motor Analítico
│   ├── cache/                        # Caché local de osmnx/geopandas
│   ├── venv/                         # Entorno virtual local (aislado)
│   ├── 01_extract_osm.py             # Extrae red vial y huellas base de OSM
│   ├── 02_extract_elevation.py       # Descarga y proyecta DEM desde Earth Engine
│   ├── 03_extract_overture.py        # Descarga huellas precisas de Overture Maps
│   ├── 04_extract_transit.py         # Ubica transporte masivo
│   ├── 05_extract_pois_roads.py      # Filtra comercio y vías principales
│   ├── 06_urban_inference_engine.py  # MOTOR MCDA: Asigna puntajes y extruye en 2.5D
│   ├── 07_download_validation_rasters.py # Extrae imágenes de GEE para comprobación
│   ├── 08_validate_inference.py      # Ejecuta el cruce estadístico final
│   └── spatial_queries.sql           # Consultas preparadas para gráficos
│
├── README.md                         # Documentación principal del proyecto
├── requirements.txt                  # Dependencias y librerías de Python
├── venv/                             # Entorno virtual general
├── .env                              # Variables de entorno y credenciales
└── .gitignore                      

## 3. Ejemplos de Gráficos e Insights Obtenidos
Para comprobar el rigor del modelo geométrico frente al mundo real, se diseñó una prueba de validación (ground-truthing). Se segmentó la ciudad en deciles, contrastando el Top 10% (los 3,865 edificios con mayor volumen inferido) contra el Bottom 10% (las 12,736 estructuras de menor escala) evaluando métricas satelitales externas:

Correlación Lumínica (VIIRS - Suomi NPP): El estrato de alta densidad (Top 10%) promedió un nivel de radiancia de 36.39, superando a las zonas de baja densidad (34.92). Esto confirma empíricamente que los clústeres donde el modelo proyectó rascacielos coinciden exactamente con la actividad económica nocturna real de la ciudad.

### Reflexiones territoriales y Siguientes Pasos
Chongqing es un laboratorio extremo, pero las condiciones que desafían su urbanización no son exclusivas de Asia. En México, existen áreas metropolitanas de topografías sumamente accidentadas (como las zonas de barrancas al poniente de la CDMX, Monterrey o Tijuana).

Aplicar este tipo de inferencia geoespacial representa un primer acercamiento al desarrollo de herramientas de geointeligencia predictiva. Al cuantificar cómo distintas variables urbanas condicionan y empujan el crecimiento vertical de una ciudad, este modelo sirve como base para la toma de decisiones estratégicas: desde la regulación y actualización de usos de suelo, hasta la evaluación para implementar nuevas líneas de transporte público y otras políticas públicas.

Los siguientes pasos para evolucionar este algoritmo incluirían la integración de datos gubernamentales cerrados, el modelado de pasarelas y puentes peatonales en grafos 3D puros, y el uso de información catastral base para expandir la matriz multicriterio, logrando una precisión más certera a nivel de parcela.

*(Para consultar algún término técnico de este repositorio, puedes revisar el [Glosario](./docs/glosario.md)).*

## 4. Instrucciones para Ejecutar
Para reproducir el motor de inferencia localmente:

1. Clona el repositorio e instala las dependencias (ver `requirements.txt`).
2. Configura la autenticación de Google Earth Engine en tu terminal ejecutando: `earthengine authenticate`.
3. Navega al directorio `scripts/` y ejecuta los archivos en orden secuencial estricto (del `01` al `08`). Los datos limpios resultantes se depositarán automáticamente en `data/processed/`.

------------------------------------------------------------------
------------------------------------------------------------------


# 2.5D Digital Twin: Spatial Inference in Chongqing

## 1. Purpose of the Analysis
The main objective of this project is to develop a geointelligence tool called the **Urban Inference Engine**, capable of modeling the latent building scale of a city by inferring buildability based on urban and territorial variables. 

The case study is the Yuzhong district peninsula in **Chongqing, China**. The choice of this site represents one of the most complex urban environments in the world due to five fundamental characteristics:
1. **Extreme topography:** Abrupt elevation changes that defy the traditional urban grid.
2. **Geographical restriction:** Physical expansion limitation due to being encapsulated by the convergence of the Yangtze and Jialing rivers.
3. **Hyper-concentrated density:** The lack of flat land forces massive vertical occupation.
4. **Three-dimensional street network:** Infrastructure adapted to the slopes that blurs the traditional notion of the "ground floor".
5. **Multilevel transit:** Monorail systems that navigate the terrain, crossing and even passing through buildings.

**Methodology** 
To calculate the buildability of over 16,000 polygons, the *Urban Inference Engine* executes the following logical flow:
- **Extracts the individual footprint** of each building downloaded from Overture Maps.
- **Calculates the specific area** of that polygon in square meters (`area_sqm`).
- **Evaluates the context:** how close that exact polygon is to the monorail (with topographical penalization), which street feeds it, and how many shops it has within a 200-meter radius.
- **Decides the number of floors and extrudes** that individual polygon into a 2.5D model.

*(To gain a deeper understanding of the theories of Spatial Economics, Space Syntax, and Multicriteria Evaluation that mathematically justify this engine, see the [Theoretical Framework](./docs/marco_teorico.md)).*

## 2. Project Structure and File Organization
The repository separates the extraction of raw data from the processed vectors that feed the frontend (Supabase / Deck.gl).
```text
03_DigitaltwinChongqing/
│
├── cache/                            # Environment cache files
│
├── data/
│   ├── raw/                          # Raw data files (Ignored in Git)
│   │   ├── 02_digitaltwin_transit.geojson # Transit nodes
│   │   ├── 03_digitaltwin_roads.geojson   # Road hierarchy
│   │   ├── 04_digitaltwin_pois.geojson    # Commercial anchors
│   │   ├── chongqingZ_buildings.geojson   # Unprocessed building footprints
│   │   └── chongqingZ_walk_network.geojson# Pedestrian network for topographic routing
│   │
│   └── processed/                    # Inferred vectors (Connection to React/Supabase)
│       └── chongqingZ_inferred_buildings.geojson # Footprints with inferred heights
│
├── docs/
│   ├── glosario.md                   # Definitions of spatial technical terms
│   └── marco_teorico.md              # Academic foundations and model formulas
│
├── scripts/                          # ETL Pipeline and Analytical Engine
│   ├── cache/                        # Local osmnx/geopandas cache
│   ├── venv/                         # Local virtual environment (isolated)
│   ├── 01_extract_osm.py             # Extracts road network and base footprints from OSM
│   ├── 02_extract_elevation.py       # Downloads and projects DEM from Earth Engine
│   ├── 03_extract_overture.py        # Downloads precise footprints from Overture Maps
│   ├── 04_extract_transit.py         # Locates mass transit
│   ├── 05_extract_pois_roads.py      # Filters commerce and main roads
│   ├── 06_urban_inference_engine.py  # MCDA ENGINE: Assigns scores and extrudes in 2.5D
│   ├── 07_download_validation_rasters.py # Extracts GEE images for verification
│   ├── 08_validate_inference.py      # Executes the final statistical cross-reference
│   └── spatial_queries.sql           # Prepared queries for charts
│
├── README.md                         # Main project documentation
├── requirements.txt                  # Python dependencies and libraries
├── venv/                             # General virtual environment
├── .env                              # Environment variables and credentials
└── .gitignore                        


```

## 3. Examples of Charts and Insights Obtained
To verify the geometric model's rigor against the real world, a validation test (ground-truthing) was designed. The city was segmented into deciles, contrasting the Top 10% (the 3,865 buildings with the highest inferred volume) against the Bottom 10% (the 12,736 smaller-scale structures) evaluating external satellite metrics:

* **Nighttime Light Correlation (VIIRS - Suomi NPP):** The high-density stratum (Top 10%) averaged a radiance level of 36.39, surpassing the low-density areas (34.92). This empirically confirms that the clusters where the model projected skyscrapers exactly match the real nighttime economic activity of the city.

### Territorial Reflections and Next Steps
Chongqing is an extreme laboratory, but the conditions that challenge its urbanization are not exclusive to Asia. In Mexico, there are metropolitan areas with highly rugged topographies (such as the ravine areas in the west of Mexico City, Monterrey, or Tijuana).

Applying this type of spatial inference represents a first approach to developing predictive geointelligence tools. By quantifying how different urban variables condition and push the vertical growth of a city, this model serves as a foundation for strategic decision-making: from the regulation and updating of land uses to the evaluation for implementing new public transit lines and other public policies.

The next steps to evolve this algorithm would include the integration of closed government data, the modeling of pedestrian walkways and bridges in pure 3D graphs, and the use of base cadastral information to expand the multicriteria matrix, achieving more accurate precision at the parcel level.

*(To consult any technical term from this repository, you can review the [Glossary](./docs/glosario.md)).*

## 4. Instructions to Run
To reproduce the inference engine locally:

1. Clone the repository and install the dependencies (see `requirements.txt`).
2. Configure the Google Earth Engine authentication in your terminal by running: `earthengine authenticate`.
3. Navigate to the `scripts/` directory and run the files in strict sequential order (from `01` to `08`). The resulting clean data will be automatically deposited in `data/processed/`.