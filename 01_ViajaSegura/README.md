# Viaja Segura: Geointeligencia y Movilidad de Cuidados en la Ruta 66

## 1. El Propósito del Análisis Realizado
El objetivo central de este proyecto es construir el sustento operativo y técnico necesario para legitimar el modelo de servicio exclusivo para mujeres e infancias de la Ruta 66 en la periferia sur de la Ciudad de México durante las horas de alta demanda. El reto principal consistió en traducir una operación social y analógica en un modelo de datos estructurado que permitiera proyectar su relevancia y expansión ante la Secretaría de Movilidad de la CDMX (SEMOVI) mediante evidencia técnica. 

La relevancia de este análisis radica en demostrar cómo la movilidad responde a la ciudad, articulando los nodos que las mujeres ya usan en su día a día. El proyecto visibiliza cómo la ubicación estratégica de servicios a distancias caminables facilita la vida cotidiana de las usuarias.

### Metodología
Para transformar el levantamiento de campo en un activo digital, el flujo de trabajo ejecutó el siguiente proceso[cite: 1]:
*   **Diseño de Instrumentos:** Creación de formatos para capturar ascensos, descensos y tiempos de recorrido en campo[cite: 1].
*   **Tratamiento y Validación (QGIS):** Limpieza de trazas geoespaciales y generación de **isocronas de 500 metros** para medir la accesibilidad peatonal[cite: 1].
*   **Cruce de Equipamiento:** Relación espacial entre paradas de alta demanda y la presencia de anclas urbanas (salud, educación y abasto)[cite: 1].
*   **Pipeline de Métricas (Python):** Automatización del cálculo de indicadores operativos y de demanda[cite: 1].

*(Para profundizar en los fundamentos de Movilidad de Cuidados y los algoritmos de accesibilidad utilizados, consulta el [Marco Teórico](./docs/marco_teorico.md).*

## 2. Estructura del Proyecto y Organización de los Archivos
El repositorio organiza los datos y scripts siguiendo un flujo de procesamiento modular[cite: 1]:

```text
01_ViajaSegura/
│
├── cache/                            # Archivos temporales del entorno
│
├── data/
│   ├── raw/                          # Datos crudos (Captura de campo y capas base)
│   │   ├── paradas_r66.json          # Geometría de paradas
│   │   └── equipamiento.json         # Capa de nodos de cuidado
│   │
│   └── processed/                    # Vectores validados para el Dashboard
│       └── metricas_demanda.geojson  # Capa final con indicadores calculados
│
├── docs/
│   ├── glosario.md                   # Definiciones de términos técnicos espaciales
│   └── marco_teorico.md              # Fundamentos de la movilidad con perspectiva de género
│
├── scripts/                          # Pipeline de procesamiento
│   ├── cache/                        # Caché de geoprocesamiento
│   ├── 01_spatial_analysis.py        # Generación de isocronas y métricas de demanda
│   └── 02_download_context.py        # Descarga de capas de contexto territorial
│
├── README.md                         # Documentación principal del proyecto
└── requirements.txt                  # Librerías y dependencias de Python
```

## 3. Ejemplos de Gráficos e Insights Obtenidos
El análisis permitió validar la ruta como un eslabón crítico en la red de movilidad de la última milla en el sur de la ciudad.  

Visualización de Impacto: A través de un dashboard interactivo, se visibiliza la dinámica del servicio, integrando los recorridos, las paradas y la dinámica de ascensos y descensos de las usuarias. Estas conexiones se vinculan con equipamientos de cuidado en distancias caminables, lo que permite tangibilizar la eficiencia del servicio en la vida diaria de las usuarias.

### Reflexiones territoriales y Siguientes Pasos
La zona de operación de la Ruta 66 se caracteriza por ser un área de periferia alta con topografía accidentada, lo que imposibilita la implementación de infraestructura masiva como Metro o Metrobús. En este contexto, el transporte público concesionado es la alternativa con mayor accesibilidad debido a su flexibilidad.

Esta herramienta pretende ser un primer acercamiento, desde una perspectiva de género e interseccionalidad, para visibilizar y tangibilizar las necesidades específicas de las usuarias de la ruta. Asimismo, se busca formalizar la labor, muchas veces no reconocida, de las asociaciones civiles que mueven a la ciudad diariamente en el transporte público concesionado de ruta.

Los siguientes pasos para evolucionar esta herramienta incluyen la integración de datos de unidades mediante GTFS para monitorización en tiempo real, así como la integración de otras rutas de transporte público concesionado y puntos de intercambio modal como Metro y Metrobús. 

*(Para consultar términos técnicos como "Viajes Encadenados" o "Isocronas", revisa el [Glosario](./docs/glosario.md)*

## 4. Instrucciones para Ejecutar
Para reproducir el análisis de métricas y geoprocesamiento localmente[cite: 1]:

1.  Clona el repositorio e instala las dependencias: `pip install -r requirements.txt`.
2.  Navega a la carpeta `scripts/`.
3.  Ejecuta `02_download_context.py` para preparar las capas territoriales.
4.  Ejecuta `01_spatial_analysis.py` para generar la capa de métricas procesadas que alimenta la visualización.


--------------------------------------------------------------------------------------------------------------------------------------------------------

# Safe Journey: Geointelligence and Care Mobility on Route 66

## 1. Purpose of the Analysis
The central objective of this project is to build the operational and technical foundation necessary to legitimize the exclusive service model for women and children on **Route 66** in the southern periphery of Mexico City during peak hours. The main challenge consisted of translating a social and analog operation into a structured data model that would allow projecting its relevance and expansion before the CDMX Ministry of Mobility (SEMOVI) through technical evidence.

The relevance of this analysis lies in demonstrating how mobility responds to the city, articulating the nodes that women already use in their daily lives. The project makes visible how the strategic location of services within walkable distances facilitates the daily lives of female users.

### Methodology
To transform field data collection into a digital asset, the workflow executed the following process:
*   **Instrument Design:** Creation of formats to capture boardings, alightings, and travel times in the field.
*   **Processing and Validation (QGIS):** Cleaning of geospatial traces and generation of **500-meter isochrones** to measure pedestrian accessibility.
*   **Equipment Cross-referencing:** Spatial relationship between high-demand stops and the presence of urban anchors (health, education, and food supply).
*   **Metrics Pipeline (Python):** Automation of the calculation for operational and demand indicators.

*(To delve deeper into the foundations of Care Mobility and the accessibility algorithms used, see the [Theoretical Framework](./docs/marco_teorico.md)).*

## 2. Project Structure and File Organization
The repository organizes data and scripts following a modular processing flow:

```text
01_ViajaSegura/
│
├── cache/                            # Environment temporary files
│
├── data/
│   ├── raw/                          # Raw data (Field capture and base layers)
│   │   ├── paradas_r66.json          # Stop geometries
│   │   └── equipamiento.json         # Care nodes layer
│   │
│   └── processed/                    # Validated vectors for the Dashboard
│       └── metricas_demanda.geojson  # Final layer with calculated indicators
│
├── docs/
│   ├── glosario.md                   # Definitions of technical spatial terms
│   └── marco_teorico.md              # Foundations of mobility with a gender perspective
│
├── scripts/                          # Processing pipeline
│   ├── cache/                        # Geoprocessing cache
│   ├── 01_spatial_analysis.py        # Generation of isochrones and demand metrics
│   └── 02_download_context.py        # Download of territorial context layers
│
├── README.md                         # Main project documentation
└── requirements.txt                  # Python libraries and dependencies
```

## 3. Examples of Charts and Insights Obtained
The analysis validated the route as a critical link in the last-mile mobility network in the south of the city.  

**Impact Visualization:** Through an interactive dashboard, the service dynamics are visualized, integrating the routes, stops, and the dynamics of user boardings and alightings. These connections are linked to care facilities within walking distances, making the service's efficiency in the daily lives of female users tangible.

### Territorial Reflections and Next Steps
The Route 66 operation zone is characterized as a high-periphery area with rugged topography, which prevents the implementation of massive infrastructure such as the Metro or Metrobús. In this context, concessioned public transport is the alternative with the greatest accessibility due to its flexibility.

This tool aims to be a first approach, from a perspective of gender and intersectionality, to visualize and make tangible the specific needs of the route's female users. Likewise, it seeks to formalize the often unrecognized work of civil associations that move the city daily via concessioned route public transport.

The next steps to evolve this tool include the integration of unit data via GTFS for real-time monitoring, as well as the integration of other concessioned public transport routes and modal exchange points such as the Metro and Metrobús. 

*(To consult technical terms such as "Trip Chaining" or "Isochrones", review the [Glossary](./docs/glosario.md)).*

## 4. Instructions to Run
To reproduce the metrics and geoprocessing analysis locally:

1.  Clone the repository and install the dependencies: `pip install -r requirements.txt`.
2.  Navigate to the `scripts/` folder.
3.  Run `02_download_context.py` to prepare the territorial layers.
4.  Run `01_spatial_analysis.py` to generate the processed metrics layer that feeds the visualization.