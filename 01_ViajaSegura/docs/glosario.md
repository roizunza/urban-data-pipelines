# Glosario de Términos Técnicos

Este documento define los conceptos clave de movilidad urbana, ciencia de datos espaciales, geografía cuantitativa y urbanismo con perspectiva de género utilizados en el proyecto **Viaja Segura** para facilitar su comprensión a perfiles no especializados.

### 1. Conceptos de Modelado y Morfología Urbana

* **Capilaridad Vial:** Capacidad de una red de transporte para penetrar en las zonas más recónditas o de difícil acceso de un territorio. En este proyecto, la Ruta 66 actúa como capilar en zonas donde el transporte masivo no puede llegar.
* **Movilidad de "Última Milla":** Se refiere al último tramo de un viaje, a menudo el más complejo, que conecta un nodo de transporte masivo (como el Metro) con el destino final del usuario.
* **Topografía Accidentada:** Terreno con pendientes pronunciadas y elevaciones irregulares. En el sur de la CDMX, esta condición actúa como una barrera física para el transporte masivo y un factor de fatiga para la movilidad peatonal.
* **Urbanismo de Proximidad:** Modelo de planificación que busca que los servicios básicos (salud, educación, comercio) estén a una distancia caminable, reduciendo la dependencia del automóvil.
* **Área de Captación (Catchment Area):** El territorio circundante a una parada de transporte desde el cual se atraen usuarios. En este modelo, se mide a través del alcance peatonal real.
* **Eje de Integración:** Función de una ruta de transporte que sirve para vincular zonas periféricas aisladas con centros de intercambio modal y equipamiento regional.

### 2. Ciencia de Datos y Algoritmos Espaciales

* **Isocrona:** Línea trazada en un mapa que une todos los puntos que son accesibles desde un centro (parada) en un tiempo o esfuerzo determinado. El proyecto utiliza isocronas de **500 metros** para simular una caminata de aproximadamente 10 minutos.
* **Análisis de Red (Network Analysis):** Cálculo de rutas basado en la geometría real de las calles y senderos, en lugar de usar radios circulares (euclidianos). Esto permite una medición exacta de la accesibilidad en terrenos con muchas barreras físicas.
* **Fricción Espacial / Topográfica:** Resistencia que el territorio impone al movimiento. En zonas de barrancas, la pendiente incrementa el "costo" del viaje a pie; el modelo considera que cada metro de desnivel vertical equivale a un esfuerzo significativamente mayor que un metro horizontal.
* **GTFS (General Transit Feed Specification):** Formato estándar internacional para datos de transporte público. Su integración permite la monitorización en tiempo real y la planificación precisa de horarios y rutas.
* **Validación Geoespacial:** Proceso de verificar en **QGIS** que las coordenadas capturadas en campo coincidan con la infraestructura existente y la traza urbana real.
* **Puntos de Carga (Hotspots):** Ubicaciones específicas (paradas) donde se registra la mayor intensidad de ascensos y descensos, indicando una alta demanda vinculada a la presencia de equipamiento urbano.

### 3. Movilidad, Género e Interseccionalidad

*   **Economía de los Cuidados:** El conjunto de actividades no remuneradas (y a veces remuneradas) necesarias para el bienestar de las personas. La Ruta 66 es el soporte físico que permite que esta economía funcione en el sur de la ciudad.
*   **Interseccionalidad:** Marco que analiza cómo diferentes identidades sociales (género, clase social, ubicación geográfica) se cruzan para crear experiencias de exclusión o privilegio en el acceso a la ciudad.
*   **Justicia Espacial:** El derecho de todos los habitantes a acceder de manera equitativa a los recursos, servicios y oportunidades que ofrece la ciudad, independientemente de su ubicación en la periferia.
*   **Movilidad de Cuidados:** Viajes realizados para realizar tareas domésticas y de cuidado de personas dependientes (niños, adultos mayores). Estos viajes suelen ser realizados mayoritariamente por mujeres.
*   **Perspectiva de Género en el Transporte:** Enfoque analítico que reconoce que hombres y mujeres usan la ciudad de manera distinta debido a roles sociales, niveles de seguridad y necesidades de movilidad.
*   **Trabajo de Cuidados:** Actividades destinadas a satisfacer las necesidades de alimentación, salud, educación y bienestar emocional de las personas (especialmente infancias, personas con discapacidad y adultos mayores), así como el mantenimiento del hogar. Este trabajo, realizado desproporcionadamente por mujeres, es el eje que genera la demanda de viajes encadenados y justifica la necesidad de transporte especializado.
*   **Viajes Encadenados (Trip Chaining):** Patrón de movilidad que consiste en realizar múltiples paradas breves y sucesivas entre el origen y el destino final (ej. hogar -> escuela -> mercado -> parada -> trabajo)

### 4. Operación y Gestión de Transporte

* **Transporte Concesionado:** Servicio de transporte público operado por particulares o asociaciones civiles bajo una concesión gubernamental. Su flexibilidad le permite adaptarse a zonas periféricas donde el Estado no tiene cobertura.
* **Intercambio Modal:** Punto donde se encuentran diferentes sistemas de transporte (ej. Ruta 66 y Metro Miguel Ángel de Quevedo), permitiendo a los usuarios cambiar de vehículo para continuar su viaje.
* **Indicadores Operativos:** Métricas matemáticas (como frecuencia de paso, ocupación por unidad y tiempos de ciclo) utilizadas para evaluar qué tan bien está funcionando un servicio de transporte.
* **Sustento Técnico:** Conjunto de datos, mapas y análisis estadísticos que validan una propuesta social ante autoridades regulatorias (como SEMOVI).

--------------------------------------------------------------------------------------------------------------------------------------------------------

# Glossary of Technical Terms

This document defines the key concepts of urban mobility, spatial data science, quantitative geography, and gender-responsive urbanism used in the **Viaja Segura** project to facilitate understanding for non-specialized profiles.

### 1. Urban Modeling and Morphology Concepts

* **Road Capillarity:** The ability of a transportation network to penetrate the most remote or difficult-to-access areas of a territory. In this project, Route 66 acts as a capillary in areas where mass transit cannot reach.
* **"Last Mile" Mobility:** Refers to the final leg of a journey, often the most complex, connecting a mass transit hub (such as the Subway) to the user's final destination.
* **Rugged Topography:** Terrain with steep slopes and irregular elevations. In southern CDMX, this condition acts as a physical barrier for mass transit and a fatigue factor for pedestrian mobility.
* **Proximity Urbanism:** A planning model that seeks to place basic services (health, education, commerce) within walking distance, reducing car dependency.
* **Catchment Area:** The surrounding territory of a transit stop from which users are drawn. In this model, it is measured through real pedestrian reach.
* **Integration Axis:** The function of a transit route that serves to link isolated peripheral areas with regional modal exchange centers and facilities.

### 2. Spatial Data Science and Algorithms

* **Isochrone:** A line drawn on a map connecting all points that are accessible from a center (stop) within a given time or effort. The project uses **500-meter** isochrones to simulate a walk of approximately 10 minutes.
* **Network Analysis:** Route calculation based on the actual geometry of streets and paths, rather than using circular (Euclidean) radii. This allows for an exact measurement of accessibility in terrains with many physical barriers.
* **Spatial / Topographic Friction:** The resistance that the territory imposes on movement. In ravine areas, the slope increases the "cost" of traveling on foot; the model considers that every meter of vertical drop is equivalent to a significantly greater effort than a horizontal meter.
* **GTFS (General Transit Feed Specification):** International standard format for public transit data. Its integration allows for real-time monitoring and precise scheduling and routing.
* **Geospatial Validation:** The process of verifying in **QGIS** that coordinates captured in the field match existing infrastructure and the actual urban layout.
* **Hotspots:** Specific locations (stops) where the highest intensity of boardings and alightings is recorded, indicating high demand linked to the presence of urban facilities.

### 3. Mobility, Gender, and Intersectionality

*   **Care Economy:** The set of unpaid (and sometimes paid) activities necessary for people's well-being. Route 66 is the physical support that allows this economy to function in the south of the city.
*   **Care Mobility:** Trips made to perform domestic tasks and care for dependents (children, elderly). These trips are usually made mostly by women.
*   **Care Work:** Activities intended to satisfy the nutritional, health, educational, and emotional well-being needs of individuals (especially children, people with disabilities, and the elderly), as well as household maintenance. This work, disproportionately performed by women, is the axis that generates the demand for trip chaining and justifies the need for specialized transportation.
*   **Gender Perspective in Transport:** An analytical approach that recognizes that men and women use the city differently due to social roles, safety levels, and mobility needs.
*   **Intersectionality:** A framework that analyzes how different social identities (gender, social class, geographical location) intersect to create experiences of exclusion or privilege in access to the city.
*   **Spatial Justice:** The right of all inhabitants to have equitable access to the resources, services, and opportunities offered by the city, regardless of their location on the periphery.
*   **Trip Chaining:** A mobility pattern consisting of making multiple brief, successive stops between the origin and the final destination (e.g., home -> school -> market -> stop -> work).

### 4. Transit Operation and Management

* **Concessioned Transport:** Public transit service operated by private individuals or civil associations under a government concession. Its flexibility allows it to adapt to peripheral areas where the state has no coverage.
* **Modal Exchange:** A point where different transportation systems meet (e.g., Route 66 and the Miguel Ángel de Quevedo Subway station), allowing users to switch vehicles to continue their journey.
* **Operational Indicators:** Mathematical metrics (such as frequency, occupancy per unit, and cycle times) used to evaluate how well a transit service is performing.
* **Technical Foundation:** The set of data, maps, and statistical analyses that validate a social proposal before regulatory authorities (such as SEMOVI).





