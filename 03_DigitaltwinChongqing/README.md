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

```text
urban-data-pipelines/
│
├── data/
│   ├── raw/                          # Archivos crudos y rasters (Ignorados en Git)
│   │   ├── chongqingZ_walk_network.geojson  # Red peatonal para ruteo topográfico
│   │   ├── chongqingZ_elevation_utm.tif     # Modelo Digital de Elevación (SRTM)
│   │   ├── chongqingZ_ndvi.tif              # Imagen Sentinel-2 (Índice de Vegetación)
│   │   └── chongqingZ_viirs.tif             # Imagen Suomi NPP (Luces Nocturnas)
│   │
│   └── processed/                    # Vectores inferidos (Conexión a React/Supabase)
│       ├── 01_digitaltwin_buildings.geojson # Huellas con alturas inferidas y validación
│       ├── 02_digitaltwin_transit.geojson   # Nodos de transporte masivo
│       ├── 03_digitaltwin_roads.geojson     # Jerarquía vial
│       └── 04_digitaltwin_pois.geojson      # Anclas comerciales y financieras
│
├── scripts/                      # Pipeline ETL y Motor Analítico
│   ├── 01_extract_osm.py             # Extrae red vial y huellas base de OSM
│   ├── 02_extract_elevation.py       # Descarga y proyecta DEM desde Earth Engine
│   ├── 03_extract_overture.py        # Descarga huellas precisas de Overture Maps
│   ├── 04_extract_transit.py         # Ubica transporte masivo
│   ├── 05_extract_pois_roads.py      # Filtra comercio y vías principales
│   ├── 06_urban_inference_engine.py  # MOTOR MCDA: Asigna puntajes y extruye en 2.5D
│   ├── 07_download_validation.py     # Extrae imágenes de GEE para comprobación
│   └── 08_validate_inference.py      # Ejecuta el cruce estadístico final por deciles
│
└── docs/
    ├── marco_teorico.md              # Fundamentos académicos y fórmulas del modelo
    └── glosario.md                   # Definiciones de términos técnicos espaciales
```

## 3. Insights Obtenidos
Para comprobar el rigor del modelo geométrico frente al mundo real, se diseñó una prueba de validación (*ground-truthing*). Se segmentó la ciudad en deciles, contrastando el **Top 10%** (los 3,865 edificios con mayor volumen inferido) contra el **Bottom 10%** (las 12,736 estructuras de menor escala) evaluando métricas satelitales externas:

* **Correlación Lumínica (VIIRS - Suomi NPP):** El estrato de alta densidad (Top 10%) promedió un nivel de radiancia de **36.39**, superando a las zonas de baja densidad (**34.92**). Esto confirma empíricamente que los clústeres donde el modelo proyectó rascacielos coinciden exactamente con la actividad económica nocturna real de la ciudad.
* **Correlación Ecológica (NDVI - Sentinel 2):** El Índice de Vegetación funcionó como freno ambiental. Las zonas inferidas con baja densidad obtuvieron un verdor significativamente mayor (**0.31**) frente a las áreas de alta densidad (**0.22**). El algoritmo respetó la orografía, confinando la escala menor a reservas ecológicas y laderas escarpadas.

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