# Simulación de escenarios de desastre: Fractura de redes y templos emergentes en Kamakura

## 1. El Propósito del Análisis Realizado

El objetivo principal de este proyecto es desarrollar una herramienta de geointeligencia denominada **Network Fracture Engine**, capaz de modelar escenarios de desastre para la gestión de riesgos urbanos y cuantificar la vulnerabilidad de la infraestructura de movilidad peatonal ante fallos sistémicos.

**Caso de Estudio: Kamakura, Japón**
La elección de esta ciudad responde a un problema geográfico crítico de riesgo costero. Kamakura es altamente propensa a sufrir tsunamis de gran magnitud debido a fallas submarinas cercanas (como la fosa de Nankai, donde el gobierno proyecta olas de impacto de hasta 14.5 metros). El verdadero peligro radica en la configuración de su terreno: la ciudad está atrapada en un "embudo", rodeada por montañas altas en tres de sus flancos y con el mar justo enfrente, lo que bloquea las rutas naturales de escape hacia el norte. Al ser un asentamiento antiguo, su malla vial es sumamente estrecha y orgánica, lo que genera cuellos de botella inmediatos y hace que una evacuación masiva sea casi imposible utilizando únicamente la infraestructura moderna actual.

**Metodología**
Para calcular el comportamiento y la resiliencia de más de 5,900 nodos viales ante el colapso territorial, el *Network Fracture Engine* ejecuta el siguiente flujo lógico:

* **Extrae la topología base** descargando la red vial y la infraestructura de templos históricos desde OpenStreetMap. Para establecer la línea de evaluación, se tomó en cuenta estrictamente la infraestructura oficial de gestión de riesgos de Japón. El algoritmo extrajo de manera exclusiva los equipamientos validados por el Estado como refugios de evacuación designados (*Shitei Hinanjo*), categorizados espacialmente como edificios públicos (`public_building`), escuelas (`school`) y ayuntamientos (`townhall`).
* **Inyecta elevación tridimensional** a cada nodo utilizando un Modelo Digital de Elevación local (`kamakura_srtm`).
* **Calcula la fricción espacial** aplicando modelos matemáticos de esfuerzo peatonal para penalizar el tiempo de evacuación en calles con pendientes pronunciadas.
* **Inunda paramétricamente** el territorio bajo diferentes escenarios extremos (10m, 20m, 30m), eliminando topológicamente las calles que quedan sumergidas.
* **Calcula rutas de evacuación de emergencia** evaluando qué calles pierden acceso a los refugios oficiales del gobierno y cuáles logran conectarse de manera emergente a un templo en zonas seguras.

*(Para conocer a profundidad las teorías sobre Teoría de Grafos, Fricción Espacial y Resiliencia Latente que justifican matemáticamente este motor, consulta el [Marco Teórico](./docs/marco_teorico.md)*

---

## 2. Estructura del Proyecto y Organización de los Archivos

El repositorio separa la extracción de datos crudos de los vectores procesados que alimentan los mapas interactivos (Mapbox / React).

```text
KamakuraNetworkFracture/
│
├── data/
│   ├── raw/                              # Archivos crudos (Ignorados en Git)
│   │   └── kamakura_srtm.tif             # Modelo Digital de Elevación local
│   │
│   └── processed/                        # Vectores inferidos (Conexión a React/Mapbox)
│       ├── kamakura_nodes.geojson        # Nodos viales extraídos
│       ├── kamakura_edges.geojson        # Segmentos de calles planos
│       ├── kamakura_official_shelters.geojson # Refugios gubernamentales de gestión de riesgos
│       ├── kamakura_emergent_temples.geojson  # Santuarios y templos históricos
│       ├── kamakura_nodes_simulated.geojson   # Resultados del motor de evacuación
│       └── kamakura_mapbox_ready.geojson # Capa optimizada para renderizado web
│
├── docs/
│   ├── glosario.md                       # Definiciones de términos técnicos espaciales
│   └── marco_teorico.md                  # Fundamentos académicos y lógicos del modelo
│
├── scripts/                              # Pipeline de Procesamiento y Simulación
│   ├── 01_extract.py                     # Minería automatizada (OSM y Overpass API)
│   ├── 02_build_graph.py                 # Construcción de grafo 3D e inyección topográfica
│   ├── 03_simulate_risk.py               # Simulación de tsunami y cálculo de rutas
│   ├── 04_export_web_pipeline.py         # Reproyección y limpieza de datos espaciales
│   └── 05_audit_levels.py                # Validación estadística de impacto
│
├── README.md                             # Documentación principal del proyecto
└── requirements.txt                      # Dependencias y librerías de Python

```

---

## 3. Ejemplos de Gráficos e Insights Obtenidos

La ejecución de la simulación a 20 metros de inundación demostró que la infraestructura oficial es insuficiente, dejando al 62.8% de la red vial desconectada. Sin embargo, el insight más valioso del modelo es el descubrimiento de una solución de gestión de riesgos basada en infraestructura preexistente: la red de templos.

El valor estratégico de este hallazgo radica en las **condiciones urbanas y espaciales específicas de los templos**. Al ser asentamientos ancestrales construidos con un profundo conocimiento del relieve, se localizan de forma nativa en cotas altas y laderas estables, contando con amplias explanadas, patios abiertos y estructuras comunitarias sólidas. Estas características arquitectónicas otorgan a los recintos una gran **flexibilidad espacial y versatilidad**, permitiendo un reuso adaptable inmediato. Significa aprovechar una infraestructura masiva que ya está construida para cambiar de ámbito de lo cultural a lo civil en minutos, funcionando como refugios temporales autónomos sin costo de edificación. El modelo comprobó que operan como anclajes orgánicos de mitigación eficientes, logrando rescatar y dar amparo a los usuarios de más de 670 calles que el Estado ya daba por perdidas.

### Reflexiones Territoriales y Siguientes Pasos

Kamakura es un laboratorio extremo de riesgo costero, pero la vulnerabilidad de las redes urbanas ante fenómenos meteorológicos no es exclusiva de Japón. En México, enfrentamos contextos de alto riesgo donde la conectividad colapsa drásticamente ante desastres climáticos, como el aislamiento topográfico de comunidades enteras en Acapulco tras el impacto de huracanes mayores, o la fractura de la red vial en las zonas periféricas de la CDMX y el Estado de México debido a inundaciones pluviales severas.

Aplicar este modelo de degradación de grafos a estos contextos representa un salto hacia la geointeligencia preventiva en la gestión de desastres. Al cuantificar dinámicamente cómo la pérdida de calles específicas aísla a la población, esta herramienta sirve como base técnica para la toma de decisiones estratégicas: desde la identificación de "refugios latentes" y reubicación de centros de acopio, hasta el rediseño de rutas operativas de emergencia (ambulancias, unidades de rescate o maquinaria de desazolve) cuando la traza principal desaparece bajo el agua.

Los siguientes pasos para evolucionar este algoritmo incluirían:

* **Integración de datos gubernamentales cerrados:** Incorporar censos demográficos a nivel parcela para transicionar de la medición de "calles conectadas" a la cuantificación exacta de población en riesgo.
* **Capacidad de Carga en Refugios:** Transicionar de un modelo de accesibilidad pura a uno de optimización de aforos, simulando la saturación y distribución logística de los equipamientos emergentes.
* **Agent-Based Modeling (ABM):** Simular flujos de multitudes interactuando en tiempo real para evaluar cuellos de botella bajo condiciones de pánico masivo.

*(Para consultar algún término técnico de este repositorio, puedes revisar el [Glosario](./docs/glosario.md)).*
---

## 4. Instrucciones para Ejecutar

Para reproducir el motor de inferencia localmente:

1. Clona el repositorio e instala las dependencias (ver `requirements.txt`).
2. Navega al directorio `scripts/` y ejecuta los archivos en orden secuencial estricto (del `01` al `05`).
3. Los datos limpios resultantes se depositarán automáticamente en `data/processed/`.


------------------------------------------------------------------
------------------------------------------------------------------

# Disaster Scenario Simulation: Network Fracture and Emergent Temples in Kamakura

## 1. The Purpose of the Analysis

The main objective of this project is to develop a geointelligence tool called the **Network Fracture Engine**, capable of modeling disaster scenarios for urban risk management and quantifying the vulnerability of pedestrian mobility infrastructure to systemic failures.

**Case Study: Kamakura, Japan**
The choice of this city responds to a critical geographic problem of coastal risk. Kamakura is highly prone to large-magnitude tsunamis due to nearby submarine faults (such as the Nankai Trough, where the government projects impact waves of up to 14.5 meters). The true danger lies in its terrain configuration: the city is trapped in a "funnel," surrounded by high mountains on three of its flanks with the sea directly in front, blocking natural escape routes to the north. Being an ancient settlement, its road network is extremely narrow and organic, generating immediate bottlenecks and making a massive evacuation almost impossible using only current modern infrastructure.

**Methodology**
To calculate the behavior and resilience of over 5,900 road nodes in the face of territorial collapse, the *Network Fracture Engine* executes the following logical flow:

* **Extracts the base topology** by downloading the road network and historical temple infrastructure from OpenStreetMap. To establish the evaluation baseline, Japan's official risk management infrastructure was strictly taken into account. The algorithm exclusively extracted the facilities validated by the State as designated evacuation shelters (*Shitei Hinanjo*), spatially categorized as public buildings (`public_building`), schools (`school`), and town halls (`townhall`).
* **Injects 3D elevation** into each node using a local Digital Elevation Model (`kamakura_srtm`).
* **Calculates spatial friction** by applying mathematical models of pedestrian effort to penalize evacuation time on streets with steep slopes.
* **Parametrically floods** the territory under different extreme scenarios (10m, 20m, 30m), topologically removing the streets that remain submerged.
* **Calculates emergency evacuation routes** by evaluating which streets lose access to official government shelters and which manage to emergently connect to a temple in safe zones.

*(To gain an in-depth understanding of the theories on Graph Theory, Spatial Friction, and Latent Resilience that mathematically justify this engine, please refer to the [Theoretical Framework](./docs/marco_teorico.md)).*

---

## 2. Project Structure and File Organization

The repository separates raw data extraction from the processed vectors that feed the interactive maps (Mapbox / React).

```text
KamakuraNetworkFracture/
│
├── data/
│   ├── raw/                              # Raw files (Ignored in Git)
│   │   └── kamakura_srtm.tif             # Local Digital Elevation Model
│   │
│   └── processed/                        # Inferred vectors (Connection to React/Mapbox)
│       ├── kamakura_nodes.geojson        # Extracted road nodes
│       ├── kamakura_edges.geojson        # Flat street segments
│       ├── kamakura_official_shelters.geojson # Official government risk management shelters
│       ├── kamakura_emergent_temples.geojson  # Historical shrines and temples
│       ├── kamakura_nodes_simulated.geojson   # Evacuation engine results
│       └── kamakura_mapbox_ready.geojson # Optimized layer for web rendering
│
├── docs/
│   ├── glosario.md                       # Definitions of spatial technical terms
│   └── marco_teorico.md                  # Academic and logical foundations of the model
│
├── scripts/                              # Processing and Simulation Pipeline
│   ├── 01_extract.py                     # Automated data mining (OSM and Overpass API)
│   ├── 02_build_graph.py                 # 3D graph construction and topographic injection
│   ├── 03_simulate_risk.py               # Tsunami simulation and route calculation
│   ├── 04_export_web_pipeline.py         # Reprojection and spatial data cleaning
│   └── 05_audit_levels.py                # Statistical impact validation
│
├── README.md                             # Main project documentation
└── requirements.txt                      # Python dependencies and libraries

```

---

## 3. Examples of Graphs and Insights Obtained

The execution of the simulation at 20 meters of flooding demonstrated that the official infrastructure is insufficient, leaving 62.8% of the road network disconnected. However, the most valuable insight of the model is the discovery of a risk management solution based on pre-existing infrastructure: the temple network.

The strategic value of this finding lies in the **specific urban and spatial conditions of the temples**. Being ancestral settlements built with a profound understanding of the relief, they are natively located at high elevations and stable hillsides, featuring large esplanades, open courtyards, and solid community structures. These architectural characteristics grant the sites great **spatial flexibility and versatility**, allowing for immediate adaptable reuse. This means leveraging massive, already-built infrastructure to shift from a cultural to a civil scope in minutes, functioning as autonomous temporary shelters with zero construction cost. The model proved that they operate as efficient organic mitigation anchors, managing to rescue and shelter users from over 670 streets that the State had already considered lost.

### Territorial Reflections and Next Steps

Kamakura is an extreme coastal risk laboratory, but the vulnerability of urban networks to meteorological phenomena is not exclusive to Japan. In Mexico, we face high-risk contexts where connectivity collapses drastically in the face of climate disasters, such as the topographic isolation of entire communities in Acapulco following the impact of major hurricanes, or the fracture of the road network in the peripheral areas of Mexico City and the State of Mexico due to severe pluvial floods.

Applying this graph degradation model to these contexts represents a leap towards preventive geointelligence in disaster management. By dynamically quantifying how the loss of specific streets isolates the population, this tool serves as a technical foundation for strategic decision-making: from identifying "latent shelters" and relocating collection centers, to redesigning operational emergency routes (ambulances, rescue units, or dredging machinery) when the main grid disappears underwater.

The next steps to evolve this algorithm would include:

* **Integration of closed government data:** Incorporate parcel-level demographic censuses to transition from measuring "connected streets" to the exact quantification of the at-risk population.
* **Shelter Carrying Capacity:** Transition from a pure accessibility model to a capacity optimization model, simulating the saturation and logistical distribution of emergent facilities.
* **Agent-Based Modeling (ABM):** Simulate crowds interacting in real-time to evaluate bottlenecks under conditions of massive panic.

*(To consult any technical term from this repository, you can review the [Glossary](./docs/glosario.md)).*

---

## 4. Instructions to Run

To reproduce the inference engine locally:

1. Clone the repository and install the dependencies (see `requirements.txt`).
2. Navigate to the `scripts/` directory and run the files in strict sequential order (from `01` to `05`).
3. The resulting clean data will be automatically deposited in `data/processed/`.

```
