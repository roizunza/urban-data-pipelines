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

* **Algoritmo de Grafos:** Conjunto de instrucciones matemáticas aplicadas a una red de nodos y bordes (calles) para calcular la ruta óptima o el costo de desplazamiento entre dos puntos.
* **Bounding Box (Caja Envolvente):** Las coordenadas rectangulares exactas (Norte, Sur, Este, Oeste) que delimitan el área de estudio para la extracción automatizada de datos espaciales.
* **Buffer Euclidiano:** Un radio circular perfecto trazado en un mapa plano desde un punto central. Suele ser inexacto en topografías complejas porque ignora el relieve y los obstáculos físicos.
* **Centroide:** El centro geométrico exacto de un polígono (la huella de un edificio). Se utiliza para simplificar el cálculo de distancias.
* **Coeficiente Restrictivo / Potenciador:** Valores aplicados en la ponderación matemática del modelo. Un coeficiente potenciador (ej. cercanía al monorraíl) multiplica el puntaje para inferir más altura; un coeficiente restrictivo (ej. pendiente de 30 grados) anula o reduce la viabilidad constructiva.
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

* **Banda 4 (Rojo Visible):** Rango del espectro electromagnético captado por satélites que corresponde a la luz roja (aprox. 665 nm), la cual es absorbida masivamente por la clorofila de las plantas.
* **Banda 8 (Infrarrojo Cercano - NIR):** Rango del espectro (aprox. 842 nm) invisible al ojo humano, pero que es fuertemente reflejado por la estructura celular interna de las hojas sanas.
* **DEM (Modelo Digital de Elevación):** Representación matricial (raster) de la superficie terrestre que contiene valores de altitud (Z) excluyendo edificios y vegetación.
* **Emisiones Lumínicas:** Radiación de luz generada artificialmente que escapa hacia la atmósfera y puede ser capturada desde el espacio.
* **Fotones:** Partículas fundamentales de la luz. Los sensores satelitales cuentan los fotones emitidos por la ciudad para calcular la intensidad de la radiancia nocturna.
* **Ground-Truthing:** Proceso de verificación empírica donde los resultados de un modelo predictivo se cruzan con datos observacionales del mundo real para comprobar su precisión.
* **Iluminación Antropogénica:** Luz artificial generada de forma continua por la actividad humana (alumbrado público, edificios comerciales, tráfico).
* **Longitud de Onda:** Distancia física entre las crestas de una onda electromagnética, utilizada para clasificar la luz captada por los sensores satelitales (visible, infrarroja, etc.).
* **NDVI (Índice de Vegetación de Diferencia Normalizada):** Indicador derivado de imágenes satelitales (Sentinel-2) que mide la salud y densidad de la biomasa vegetal. El modelo lo utiliza como freno para comprobar que no se proyectaron rascacielos sobre reservas naturales.
* **Percepción Remota / Teledetección:** Ciencia de adquirir información sobre la superficie terrestre sin contacto físico, típicamente mediante el uso de sensores a bordo de satélites o aeronaves.
* **Sensor DNB (Day/Night Band):** Instrumento especializado a bordo del satélite Suomi NPP, altamente sensible para capturar emisiones lumínicas durante la noche.
* **VIIRS (Visible Infrared Imaging Radiometer Suite):** Instrumento a bordo del satélite Suomi NPP capaz de capturar luz visible por la noche. Se utiliza para mapear la intensidad de la iluminación humana y validar empíricamente los núcleos de alta densidad.

### 4. Estadística y Economía

* **Correlación Matemática Lineal:** Relación estadística entre dos variables donde el cambio en una se asocia con un cambio proporcional en la otra (ej. a mayor luz nocturna, mayor densidad inferida).
* **Decil:** Segmentación estadística que divide un conjunto de datos ordenados en 10 partes iguales. Evaluar el modelo contrastando el decil superior (Top 10%) contra el inferior (Bottom 10%) permite comparar los extremos absolutos (rascacielos masivos vs. viviendas precarias) para validar su precisión.
* **Econometría Espacial:** Rama de la economía que aplica métodos estadísticos a datos que tienen componentes espaciales o geográficos para identificar dependencias y tendencias territoriales.
* **Estadística Paramétrica:** Rama de la estadística que asume que los datos analizados provienen de un tipo de distribución de probabilidad subyacente, permitiendo inferencias matemáticas precisas.
* **PIB (Producto Interno Bruto):** Medida macroeconómica que expresa el valor monetario de la producción de bienes y servicios. En este proyecto, la luz nocturna funciona como un proxy espacial del PIB local.