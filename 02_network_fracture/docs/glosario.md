# Glosario de Términos Técnicos

Este documento define los conceptos clave de geografía cuantitativa, ciencia de redes, modelado topográfico y gestión del riesgo de desastres utilizados a lo largo del proyecto para facilitar su comprensión a perfiles no especializados.

### 1. Conceptos de Modelado y Morfología Urbana

* **Cuello de Botella (Bottleneck):** Estrechamiento físico o topológico en la red vial que restringe severamente la capacidad de flujo peatonal, provocando aglomeraciones peligrosas durante evacuaciones masivas.
* **Déficit Oficial:** Métrica que cuantifica el límite operativo del Estado. Representa el porcentaje exacto de la ciudad y de la población que queda fuera de la zona de cobertura del plan de respuesta a emergencias moderno debido a la pérdida de conectividad.
* **Encapsulamiento Orográfico:** Condición geográfica donde un asentamiento urbano se encuentra rodeado y bloqueado por barreras naturales abruptas (como cadenas montañosas o acantilados), limitando severamente las rutas de escape terrestre.
* **Fractura de Red (Network Fracture):** Rompimiento de la continuidad estructural de la traza urbana debido a la destrucción o sumersión de sus calles, transformando un tejido interconectado en múltiples clústeres aislados.
* **Infraestructura Emergente:** Activos urbanos (como templos y santuarios históricos) que no fueron diseñados contemporáneamente para la protección civil, pero que por su ubicación estratégica, solidez y amplitud asumen roles críticos de refugio durante el colapso del sistema oficial.
* **Malla Vial Histórica:** Trazado urbano heredado de épocas antiguas (como el período medieval en Kamakura), caracterizado por calles orgánicas, sinuosas y estrechas que incrementan la fricción y dificultan las logísticas modernas de evacuación.
* **Refugio de Evacuación Designado (*Shitei Hinanjo*):** Equipamiento público validado y oficializado por el gobierno de Japón (escuelas, ayuntamientos, centros comunitarios) destinado a albergar a la población durante y después de un desastre natural.
* **Run-up (Altura de Inundación):** La máxima altitud topográfica que alcanza el agua de un tsunami tierra adentro sobre el nivel del mar, utilizada para calibrar los umbrales de estrés del modelo.

### 2. Ciencia de Datos y Algoritmos de Redes

* **Algoritmo de Dijkstra:** Algoritmo matemático empleado en la teoría de grafos para encontrar la ruta más corta (o de menor costo/esfuerzo) desde un nodo de origen hacia todos los demás nodos o hacia un destino específico dentro de una red ponderada.
* **Arista (Edge):** En la teoría de redes, representa el vector o línea que conecta dos puntos. En este proyecto, cada arista es un segmento de calle transitable peatonalmente.
* **Capacidad de Absorción:** El porcentaje matemático del impacto territorial crítico (calles desconectadas) que logra ser contenido, enrutado y solucionado de manera orgánica por la red de infraestructura patrimonial emergente.
* **Costo de Viaje (Weight / Cost):** Valor numérico asignado a cada arista del grafo que no representa distancia, sino el nivel de "esfuerzo físico" o "tiempo" requerido para transitarla, penalizando aquellas rutas con pendientes empinadas.
* **Grafo Topológico Dirigido:** Representación matemática estricta de la red vial mediante nodos y aristas interconectados. Al ser "dirigido", permite modelar el flujo en sentidos específicos y recalcular trayectorias cuando una sección de la red es eliminada.
* **Network Fracture Engine:** Motor algorítmico paramétrico desarrollado en este proyecto, diseñado para simular escenarios de desastre, degradar grafos topológicos y auditar la vulnerabilidad de la movilidad de emergencia.
* **Nodo Aislado / Huérfano (Orphan Node):** Punto de intersección vial que, tras la simulación de un nivel de inundación específico y la ruptura del grafo, pierde por completo su ruta de acceso hacia la red de refugios oficiales.
* **Nodo Rescatado (Rescued Node):** Intersección que, habiendo perdido acceso al plan de evacuación gubernamental, logra restablecer una ruta de escape viable gracias a la proximidad y altitud de un templo histórico operativo.
* **Simulación Paramétrica:** Ejecución iterativa de un modelo informático donde se modifican variables de entrada específicas (como elevar el umbral de inundación de 10m a 20m y 30m) para observar y cuantificar las variaciones en el comportamiento de la red.
* **Vértice (Node):** Unidad mínima en un grafo. En el modelo urbano, representa las intersecciones de las calles o los callejones sin salida donde los peatones pueden tomar decisiones de enrutamiento.

### 3. Geoinformática y Topografía

* **DEM (Modelo Digital de Elevación):** Representación matricial (raster) de la superficie terrestre que almacena valores precisos de altitud (Z) sobre el nivel del mar.
* **Fricción Espacial / Topográfica:** Resistencia invisible que el relieve impone sobre el movimiento humano. Subir una colina empinada requiere mayor esfuerzo energético que caminar en llano, alterando drásticamente el área real de accesibilidad peatonal.
* **Función de Excursionismo de Tobler (Tobler's Hiking Function):** Ecuación matemática exponencial formulada en la geografía cuantitativa que calcula la velocidad de marcha de un peatón basándose en la inclinación exacta del terreno.
* **Geointeligencia Preventiva:** Aplicación del análisis de datos espaciales y simulaciones computacionales para predecir vulnerabilidades territoriales antes de que ocurra un evento catastrófico, facilitando la planificación proactiva.
* **Raster vs. Vector:** Formatos de datos espaciales. El *Raster* es una cuadrícula de píxeles (usado aquí para el modelo de altitud), mientras que el *Vector* utiliza puntos, líneas y polígonos matemáticos (usado aquí para mapear calles y refugios).

### 4. Gestión del Riesgo y Resiliencia

* **Agent-Based Modeling (ABM):** Técnica de simulación computacional donde "agentes" individuales (peatones virtuales) interactúan en un entorno bajo reglas predefinidas, utilizada para predecir dinámicas complejas de multitudes, pánico y cuellos de botella.
* **DRR (Disaster Risk Reduction):** Disciplina global sistemática que busca identificar, evaluar y reducir los riesgos de desastres, minimizando las vulnerabilidades sociales y físicas del entorno construido.
* **Resiliencia Latente / Orgánica:** Capacidad intrínseca y no planificada de un territorio o comunidad para absorber un impacto catastrófico. En este proyecto, se refiere a la inteligencia espacial de los recintos ancestrales para fungir como anclajes de supervivencia sin requerir inversión en infraestructura nueva.
* **Vulnerabilidad Sistémica:** Falla en cadena donde el colapso de un componente del entorno urbano (una avenida principal inundada) provoca la inutilidad operativa de todo el sistema de respuesta de emergencias de esa zona.

---

# Glossary of Technical Terms

This document defines the key concepts of quantitative geography, network science, topographic modeling, and disaster risk management used throughout the project to facilitate understanding for non-specialized profiles.

### 1. Urban Modeling and Risk Concepts

* **Bottleneck:** Physical or topological narrowing in the road network that severely restricts pedestrian flow capacity, causing dangerous crowding during massive evacuations.
* **Official Deficit:** Metric that quantifies the operational limit of the State. It represents the exact percentage of the city and population that falls outside the coverage area of the modern emergency response plan due to connectivity loss.
* **Orographic Encapsulation:** Geographic condition where an urban settlement is surrounded and blocked by abrupt natural barriers (such as mountain ranges or cliffs), severely limiting land escape routes.
* **Network Fracture:** Breakdown of the structural continuity of the urban fabric due to the destruction or submersion of its streets, transforming an interconnected tissue into multiple isolated clusters.
* **Emergent Infrastructure:** Urban assets (such as historical temples and shrines) that were not contemporarily designed for civil protection, but due to their strategic location, solidity, and spaciousness, assume critical shelter roles during the collapse of the official system.
* **Historical Road Network:** Urban layout inherited from ancient eras (such as the medieval period in Kamakura), characterized by organic, winding, and narrow streets that increase friction and hinder modern evacuation logistics.
* **Designated Evacuation Shelter (*Shitei Hinanjo*):** Public facility validated and officialized by the Japanese government (schools, town halls, community centers) intended to house the population during and after a natural disaster.
* **Run-up:** The maximum topographic elevation that a tsunami's water reaches inland above sea level, used to calibrate the model's stress thresholds.

### 2. Data Science and Network Algorithms

* **Dijkstra's Algorithm:** Mathematical algorithm used in graph theory to find the shortest (or lowest cost/effort) path from a source node to all other nodes or a specific destination within a weighted network.
* **Edge:** In network theory, it represents the vector or line connecting two points. In this project, each edge is a pedestrian-navigable street segment.
* **Absorption Capacity:** The mathematical percentage of the critical territorial impact (disconnected streets) that manages to be contained, routed, and organically solved by the emergent heritage infrastructure network.
* **Weight / Cost:** Numerical value assigned to each edge of the graph that does not represent distance, but the level of "physical effort" or "time" required to transit it, penalizing routes with steep slopes.
* **Directed Topological Graph:** Strict mathematical representation of the road network using interconnected nodes and edges. Being "directed," it allows modeling flow in specific directions and recalculating trajectories when a section of the network is removed.
* **Network Fracture Engine:** Parametric algorithmic engine developed in this project, designed to simulate disaster scenarios, degrade topological graphs, and audit emergency mobility vulnerability.
* **Orphan / Isolated Node:** Street intersection point that, following the simulation of a specific flood level and the fracture of the graph, completely loses its access route to the official shelter network.
* **Rescued Node:** Intersection that, having lost access to the government evacuation plan, manages to re-establish a viable escape route thanks to the proximity and altitude of an operational historical temple.
* **Parametric Simulation:** Iterative execution of a computer model where specific input variables are modified (such as raising the flood threshold from 10m to 20m and 30m) to observe and quantify variations in network behavior.
* **Node (Vertex):** The minimum unit in a graph. In the urban model, it represents street intersections or dead ends where pedestrians can make routing decisions.

### 3. Geoinformatics and Topography

* **DEM (Digital Elevation Model):** Matrix representation (raster) of the Earth's surface that stores precise altitude values (Z) above sea level.
* **Spatial / Topographic Friction:** Invisible resistance that the relief imposes on human movement. Climbing a steep hill requires more energy effort than walking on flat ground, drastically altering the actual area of pedestrian accessibility.
* **Tobler's Hiking Function:** Exponential mathematical equation formulated in quantitative geography that calculates a pedestrian's walking speed based on the exact inclination of the terrain.
* **Preventive Geointelligence:** Application of spatial data analysis and computer simulations to predict territorial vulnerabilities before a catastrophic event occurs, facilitating proactive planning.
* **Raster vs. Vector:** Spatial data formats. *Raster* is a grid of pixels (used here for the altitude model), while *Vector* uses mathematical points, lines, and polygons (used here to map streets and shelters).

### 4. Risk Management and Resilience

* **Agent-Based Modeling (ABM):** Computer simulation technique where individual "agents" (virtual pedestrians) interact in an environment under predefined rules, used to predict complex crowd dynamics, panic, and bottlenecks.
* **DRR (Disaster Risk Reduction):** Systematic global discipline that seeks to identify, evaluate, and reduce disaster risks, minimizing the social and physical vulnerabilities of the built environment.
* **Latent / Organic Resilience:** Intrinsic and unplanned capacity of a territory or community to absorb a catastrophic impact. In this project, it refers to the spatial intelligence of ancestral sites to serve as survival anchors without requiring investment in new infrastructure.
* **Systemic Vulnerability:** Chain failure where the collapse of one component of the urban environment (a flooded main avenue) causes the operational futility of the entire emergency response system in that area.

