# Glosario de Términos Técnicos

Este documento define los conceptos clave de geografía cuantitativa, ciencia de datos espaciales, teledetección y economía urbana utilizados a lo largo del proyecto para facilitar su comprensión a perfiles no especializados.

### 1. Conceptos de Modelado y Morfología Urbana

* **Capacidad de Carga Vial:** El volumen máximo de flujo vehicular y peatonal que una calle puede soportar. En el modelo, dicta si una vía tiene la infraestructura necesaria para sostener desarrollos de alta densidad.
* **Densidad Hiperconcentrada:** Ocupación masiva del espacio en áreas muy reducidas, forzando la verticalización extrema de la arquitectura debido a la escasez de suelo urbanizable.
* **Desarrollo Orientado al Transporte (TOD):** Paradigma de planificación urbana que busca maximizar la cantidad de espacio residencial, comercial y de ocio a una distancia caminable del transporte público masivo.
* **Extrusión 2.5D:** Técnica de modelado que toma polígonos planos de dos dimensiones (huellas de edificios) y los proyecta verticalmente asignándoles un único valor de altura (Eje Z). A diferencia del 3D puro, no modela geometrías complejas como volados, túneles o pasarelas superpuestas.
* **Gemelo Digital (Digital Twin):** Réplica virtual de un entorno físico (en este caso, la ciudad de Chongqing). En este proyecto, no es solo un modelo 3D visual, sino un entorno de datos conectado a algoritmos que simulan el comportamiento y las restricciones del mundo real.
* **Parcela:** Polígono o lote de terreno que representa la unidad mínima de división del suelo, sobre la cual se desplanta la huella de un edificio.
* **Rascacielos:** Edificio de gran altura(generalmente superior a 40 niveles en este contexto) que actúa como ancla de densidad, habitualmente asociado a distritos financieros o comerciales.
* **Restricción Geográfica:** Limitaciones físicas impuestas por la naturaleza (ríos, barrancas, océanos) que impiden la expansión horizontal de una ciudad.
* **Topografía Extrema:** Terreno caracterizado por cambios de elevación abruptos y pendientes pronunciadas que imposibilitan el trazado de una cuadrícula urbana tradicional.
* **Trama Vial Tridimensional:** Red de calles y autopistas que, para adaptarse al relieve escarpado, se superpone en múltiples niveles a través de viaductos, puentes y túneles.
* **Transporte Multinivel:** Sistemas de movilidad masiva (como el monorraíl) que operan en diferentes ejes de altura, cruzando valles e incluso atravesando estructuras arquitectónicas.
* **Red Vial (Primaria, Secundaria y Local):** Clasificación jerárquica de las calles. Las vías *primarias* soportan flujos a gran escala y usos mixtos; las *secundarias* conectan distritos; y las *locales* restringen la velocidad y el tráfico, asociándose a usos residenciales de menor escala.

### 2. Ciencia de Datos y Algoritmos Espaciales

* **Índice Espacial (K-D Tree) y Factor de Desvío:** En lugar de trazar rutas paso a paso por cada calle, el modelo utiliza un árbol K-D (K-Dimensional Tree) para encontrar matemáticamente el nodo de transporte más cercano a cada polígono. Para simular que los peatones no vuelan y deben caminar por las banquetas, esta distancia recta (euclidiana) se multiplica por un coeficiente de desvío (detour index), emulando la geometría de la trama urbana.index), emulando la geometría de la trama urbana.
* **Bounding Box (Caja Envolvente):** Las coordenadas rectangulares exactas (Norte, Sur, Este, Oeste) que delimitan el área de estudio para la extracción automatizada de datos espaciales.
* **Buffer Euclidiano:** Un radio circular perfecto trazado en un mapa plano desde un punto central. Suele ser inexacto en topografías complejas porque ignora el relieve y los obstáculos físicos.
* **Centroide:** El centro geométrico exacto de un polígono (la huella de un edificio). Se utiliza para simplificar el cálculo de distancias.
* **Coeficiente Restrictivo / Potenciador:** Valores aplicados en la ponderación matemática del modelo. Un coeficiente potenciador (ej. tener una estación de monorraíl muy cerca) incrementa el puntaje para inferir más altura; un coeficiente restrictivo (ej. estar ubicado sobre una calle local de baja capacidad) reduce drásticamente el puntaje final, bloqueando la viabilidad de inferir un rascacielos.
* **Evaluación Multicriterio Espacial (Spatial MCDA):** Técnica de toma de decisiones que evalúa un mismo elemento (un lote) bajo varias reglas espaciales simultáneamente. Funciona como un sistema de puntuación donde el terreno gana o pierde viabilidad constructiva dependiendo de sus ventajas comerciales, viales y topográficas.
* **Fricción Topográfica / Espacial:** Resistencia al movimiento peatonal causada por la pendiente del terreno. En el modelo, subir una colina empinada cuesta más "esfuerzo" o energía que caminar en plano, reduciendo el área real de cobertura y accesibilidad de una estación de transporte.
* **Geointeligencia:** Uso de tecnologías de información geográfica, algoritmos y bases de datos espaciales para analizar problemas territoriales complejos y orientar la toma de decisiones.
* **Inferencia Espacial:** Proceso analítico que utiliza algoritmos matemáticos para predecir o estimar información faltante (como la altura de un edificio) basándose en las pistas y variables de su entorno territorial inmediato.
* **Integración Topológica:** Métrica de la Sintaxis Espacial que evalúa qué tan conectada o aislada está una calle específica dentro del tejido total de la ciudad.
* **POIs (Puntos de Interés):** Ubicaciones vectoriales específicas en un mapa que representan una función o actividad útil en la ciudad. El algoritmo filtra POIs estrictamente financieros, comerciales y turísticos para localizar los nodos de mayor presión inmobiliaria.
* **Proxy (Variable Proxy):** Dato indirecto o sustituto que se utiliza para medir una variable abstracta o difícil de calcular. En este modelo, utilizamos la "Luz Nocturna" (radiancia) como un proxy para medir la "Actividad Económica" y concentración de capital.
* **Raster:** Imagen digital espacial compuesta por una matriz o cuadrícula de píxeles, donde cada píxel almacena un valor matemático continuo. Ejemplos en este proyecto incluyen el Modelo de Elevación (valores de altura) o las imágenes de satélite (valores de reflectancia).
* **Urban Inference Engine:** Motor algorítmico paramétrico desarrollado en este proyecto, diseñado para estimar variables morfológicas urbanas (como la altura constructiva) a partir del cruce de datos espaciales.

### 3. Teledetección y Percepción Remota

* **DEM (Modelo Digital de Elevación):** Representación matricial (raster) de la superficie terrestre que contiene valores de altitud (Z) excluyendo edificios y vegetación.
* **Emisiones Lumínicas:** Radiación de luz generada artificialmente que escapa hacia la atmósfera y puede ser capturada desde el espacio.
* **Fotones:** Partículas fundamentales de la luz. Los sensores satelitales cuentan los fotones emitidos por la ciudad para calcular la intensidad de la radiancia nocturna.
* **Ground-Truthing:** Proceso de verificación empírica donde los resultados de un modelo predictivo se cruzan con datos observacionales del mundo real para comprobar su precisión.
* **Iluminación Antropogénica:** Luz artificial generada de forma continua por la actividad humana (alumbrado público, edificios comerciales, tráfico).
* **Longitud de Onda:** Distancia física entre las crestas de una onda electromagnética, utilizada para clasificar la luz captada por los sensores satelitales (visible, infrarroja, etc.).
* **Percepción Remota / Teledetección:** Ciencia de adquirir información sobre la superficie terrestre sin contacto físico, típicamente mediante el uso de sensores a bordo de satélites o aeronaves.
* **Sensor DNB (Day/Night Band):** Instrumento especializado a bordo del satélite Suomi NPP, altamente sensible para capturar emisiones lumínicas durante la noche.
* **VIIRS (Visible Infrared Imaging Radiometer Suite):** Instrumento a bordo del satélite Suomi NPP capaz de capturar luz visible por la noche. Se utiliza para mapear la intensidad de la iluminación humana y validar empíricamente los núcleos de alta densidad.

### 4. Estadística y Economía

* **Correlación Matemática Lineal:** Relación estadística entre dos variables donde el cambio en una se asocia con un cambio proporcional en la otra (ej. a mayor luz nocturna, mayor densidad inferida).
* **Decil:** Segmentación estadística que divide un conjunto de datos ordenados en 10 partes iguales. Evaluar el modelo contrastando el decil superior (Top 10%) contra el inferior (Bottom 10%) permite comparar los extremos absolutos (rascacielos masivos vs. viviendas precarias) para validar su precisión.
* **Econometría Espacial:** Rama de la economía que aplica métodos estadísticos a datos que tienen componentes espaciales o geográficos para identificar dependencias y tendencias territoriales.
* **Estadística Paramétrica:** Rama de la estadística que asume que los datos analizados provienen de un tipo de distribución de probabilidad subyacente, permitiendo inferencias matemáticas precisas.
* **PIB (Producto Interno Bruto):** Medida macroeconómica que expresa el valor monetario de la producción de bienes y servicios. En este proyecto, la luz nocturna funciona como un proxy espacial del PIB local.


------------------------------------------------------------------------------------------------------------------------------------------


# Glossary of Technical Terms

This document defines the key concepts of quantitative geography, spatial data science, remote sensing, and urban economics used throughout the project to facilitate understanding for non-specialized profiles.

### 1. Urban Modeling and Morphology Concepts

* **Road Carrying Capacity:** The maximum volume of vehicular and pedestrian flow that a street can support. In the model, it dictates whether a road has the necessary infrastructure to sustain high-density developments.
* **Hyper-concentrated Density:** Massive space occupation in very reduced areas, forcing extreme architectural verticalization due to the scarcity of developable land.
* **Transit-Oriented Development (TOD):** Urban planning paradigm that seeks to maximize the amount of residential, commercial, and leisure space within a walkable distance of mass public transit.
* **2.5D Extrusion:** Modeling technique that takes flat two-dimensional polygons (building footprints) and projects them vertically by assigning them a single height value (Z-Axis). Unlike pure 3D, it does not model complex geometries such as overhangs, tunnels, or overlapping walkways.
* **Digital Twin:** Virtual replica of a physical environment (in this case, the city of Chongqing). In this project, it is not just a visual 3D model, but a data environment connected to algorithms that simulate real-world behavior and restrictions.
* **Parcel (Plot):** Polygon or plot of land representing the minimum unit of land division, upon which a building's footprint is placed.
* **Skyscraper:** High-rise building (generally over 40 stories in this context) that acts as a density anchor, usually associated with financial or commercial districts.
* **Geographical Restriction:** Physical limitations imposed by nature (rivers, ravines, oceans) that prevent a city's horizontal expansion.
* **Extreme Topography:** Terrain characterized by abrupt elevation changes and steep slopes that make mapping a traditional urban grid impossible.
* **Three-dimensional Street Network:** Network of streets and highways that, to adapt to the steep terrain, overlaps on multiple levels through viaducts, bridges, and tunnels.
* **Multilevel Transit:** Mass mobility systems (such as the monorail) that operate on different height axes, crossing valleys and even passing through architectural structures.
* **Road Network (Primary, Secondary, and Local):** Hierarchical classification of streets. *Primary* roads support large-scale flows and mixed uses; *secondary* ones connect districts; and *local* ones restrict speed and traffic, being associated with smaller-scale residential uses.

### 2. Spatial Data Science and Algorithms

* **Spatial Index (K-D Tree) and Detour Factor:** Instead of tracing step-by-step routes through each street, the model uses a K-D (K-Dimensional) Tree to mathematically find the closest transit node to each polygon. To simulate that pedestrians do not fly and must walk along sidewalks, this straight-line (Euclidean) distance is multiplied by a detour coefficient (*detour index*), emulating the geometry of the urban fabric.
* **Bounding Box:** The exact rectangular coordinates (North, South, East, West) that delimit the study area for automated spatial data extraction.
* **Euclidean Buffer:** A perfect circular radius drawn on a flat map from a central point. It is often inaccurate in complex topographies because it ignores terrain and physical obstacles.
* **Centroid:** The exact geometric center of a polygon (a building's footprint). It is used to simplify distance calculations.
* **Restrictive / Enhancing Coefficient:** Values applied in the model's mathematical weighting. An enhancing coefficient (e.g., having a monorail station very close) increases the score to infer more height; a restrictive coefficient (e.g., being located on a low-capacity local street) drastically reduces the final score, blocking the viability of inferring a skyscraper.
* **Spatial Multicriteria Evaluation (Spatial MCDA):** Decision-making technique that evaluates the same element (a plot) under several spatial rules simultaneously. It works as a scoring system where the land gains or loses constructability viability depending on its commercial, road, and topographic advantages.
* **Topographic / Spatial Friction:** Resistance to pedestrian movement caused by terrain slope. In the model, climbing a steep hill costs more "effort" or energy than walking on flat ground, reducing a transit station's actual coverage area and accessibility.
* **Geointelligence:** Use of geographic information technologies, algorithms, and spatial databases to analyze complex territorial problems and guide decision-making.
* **Spatial Inference:** Analytical process that uses mathematical algorithms to predict or estimate missing information (such as a building's height) based on clues and variables from its immediate territorial surroundings.
* **Topological Integration:** Space Syntax metric that evaluates how connected or isolated a specific street is within the city's overall fabric.
* **POIs (Points of Interest):** Specific vector locations on a map representing a useful function or activity in the city. The algorithm filters strictly financial, commercial, and tourist POIs to locate the nodes with the highest real estate pressure.
* **Proxy (Proxy Variable):** Indirect or substitute data used to measure an abstract or difficult-to-calculate variable. In this model, we use "Nighttime Light" (radiance) as a proxy to measure "Economic Activity" and capital concentration.
* **Raster:** Spatial digital image composed of a matrix or grid of pixels, where each pixel stores a continuous mathematical value. Examples in this project include the Elevation Model (height values) or satellite images (reflectance values).
* **Urban Inference Engine:** Parametric algorithmic engine developed in this project, designed to estimate urban morphological variables (such as building height) by cross-referencing spatial data.

### 3. Remote Sensing

* **DEM (Digital Elevation Model):** Matrix representation (raster) of the Earth's surface containing altitude values (Z), excluding buildings and vegetation.
* **Light Emissions:** Artificially generated light radiation that escapes into the atmosphere and can be captured from space.
* **Photons:** Fundamental particles of light. Satellite sensors count the photons emitted by the city to calculate the intensity of nighttime radiance.
* **Ground-Truthing:** Empirical verification process where a predictive model's results are cross-referenced with observational real-world data to verify its accuracy.
* **Anthropogenic Lighting:** Artificial light continuously generated by human activity (street lighting, commercial buildings, traffic).
* **Wavelength:** Physical distance between the crests of an electromagnetic wave, used to classify the light captured by satellite sensors (visible, infrared, etc.).
* **Remote Sensing:** Science of acquiring information about the Earth's surface without physical contact, typically using sensors aboard satellites or aircraft.
* **DNB (Day/Night Band) Sensor:** Specialized instrument aboard the Suomi NPP satellite, highly sensitive to capturing light emissions at night.
* **VIIRS (Visible Infrared Imaging Radiometer Suite):** Instrument aboard the Suomi NPP satellite capable of capturing visible light at night. It is used to map the intensity of human illumination and empirically validate high-density cores.

### 4. Statistics and Economics

* **Linear Mathematical Correlation:** Statistical relationship between two variables where a change in one is associated with a proportional change in the other (e.g., the more nighttime light, the higher the inferred density).
* **Decile:** Statistical segmentation that divides a set of ordered data into 10 equal parts. Evaluating the model by contrasting the upper decile (Top 10%) against the lower (Bottom 10%) allows comparing absolute extremes (massive skyscrapers vs. precarious housing) to validate its accuracy.
* **Spatial Econometrics:** Branch of economics that applies statistical methods to data with spatial or geographic components to identify territorial dependencies and trends.
* **Parametric Statistics:** Branch of statistics that assumes the analyzed data comes from an underlying probability distribution type, allowing for precise mathematical inferences.
* **GDP (Gross Domestic Product):** Macroeconomic measure expressing the monetary value of the production of goods and services. In this project, nighttime light serves as a spatial proxy for local GDP.