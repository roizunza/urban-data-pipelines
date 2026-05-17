¡Tienes toda la razón, Rocío! Entendí perfecto el golpe. Me desvié del formato exacto que querías y te di una mezcla rara. Viendo nuevamente tu documento de Chongqing, la estructura es clarísima: un párrafo introductorio contundente que define el motor y las disciplinas que lo nutren, seguido de los conceptos numerados en negritas donde explicamos la teoría y luego **cómo se traduce eso en matemáticas o reglas dentro del código**.

Borrón y cuenta nueva. Aquí tienes el **Marco Teórico** de Kamakura calcado exactamente con el rigor, el ritmo y el formato de tu proyecto de Chongqing, primero en español y luego en inglés.

---

# Marco Teórico y Fundamentos Analíticos

El presente proyecto emplea el *Network Fracture Engine*, el cual se define como un motor algorítmico diseñado para auditar la resiliencia territorial y simular la degradación de redes de movilidad ante catástrofes naturales (tsunamis). Su funcionamiento no es aleatorio; se fundamenta en teorías consolidadas provenientes de diversos ámbitos, tales como la geografía cuantitativa, la gestión del riesgo de desastres (DRR) y la ciencia de redes. Asimismo, integra metodologías de disciplinas analíticas complejas —como el modelado topológico tridimensional y el cálculo vectorial espacial— para lograr un acercamiento y decodificar la vulnerabilidad sistémica del territorio urbano.

A continuación, se explican las teorías de las que se nutre el algoritmo para funcionar:

**1. Topología Urbana y Teoría de Grafos (Graph Theory vs. Space Syntax)**
Para modelar la infraestructura de evacuación, el modelo descarta la proximidad euclidiana plana y los fundamentos tradicionales de la Sintaxis Espacial (*Space Syntax*). Mientras que la Sintaxis Espacial es óptima para predecir flujos peatonales orgánicos en condiciones de "normalidad" basándose en la visibilidad y la integración urbana, una evacuación por desastre exige calcular flujos forzados bajo estrés físico absoluto. Por ello, el motor se construye sobre la **Teoría de Grafos**. En el modelo, la traza vial se reconstruye matemáticamente como un grafo topológico dirigido $G = (V, E)$, donde las intersecciones son vértices ($V$) y los segmentos de calle son aristas ($E$). Esto permite que el algoritmo evalúe la ciudad como una red estructural, donde la pérdida física de una arista altera la conectividad y el costo operativo de todo el sistema.

**2. Fricción Espacial y Esfuerzo Peatonal (Tobler's Hiking Function)**
Para modelar el desplazamiento peatonal hacia los refugios, el algoritmo rechaza los "buffers circulares" convencionales, ya que en la topografía accidentada de Kamakura, aplicar radios lineales resulta en una interpretación engañosa del riesgo. Por ello, el algoritmo aplica el concepto de **Fricción Espacial**. Utilizando Modelos Digitales de Elevación locales (DEM), el motor inyecta la cota altimétrica ($Z$) a cada nodo del grafo para calcular la pendiente de cada calle. Posteriormente, aplica la **Función de Excursionismo de Tobler** (*Tobler's Hiking Function*), una ecuación empírica que penaliza el esfuerzo de movimiento basándose en la inclinación. El algoritmo traduce la geometría tridimensional en un coeficiente de tiempo de viaje ($T$), penalizando matemáticamente las laderas empinadas y demostrando que un refugio visualmente cercano puede resultar operativamente inaccesible debido a la fricción orográfica.

**3. Vulnerabilidad Sistémica y Enrutamiento de Costo Mínimo (Dijkstra's Algorithm)**
Para integrar las variables de riesgo y evaluar el límite operativo de la protección civil, el modelo emplea simulaciones de estrés paramétrico (10m, 20m, 30m de inundación). Durante la simulación, el código evalúa la cota mínima de cada arista vial ($Z_{\text{min}}$); si el nivel del agua supera esta cota, la arista se elimina del grafo, simulando la pérdida física del camino.
Sobre esta red fracturada, el algoritmo ejecuta cálculos de accesibilidad utilizando el **Algoritmo de Dijkstra**, buscando la ruta de menor costo de esfuerzo (basado en Tobler) desde cada punto hacia los refugios oficiales del Estado. Si el vector resultante hacia la red gubernamental arroja un costo infinito ($d \to \infty$), el motor penaliza el nodo catalogándolo como "Nodo Aislado", revelando así el déficit de cobertura real de la política pública.

**4. Resiliencia Latente e Infraestructura Emergente**
La validación de la hipótesis central del proyecto se fundamenta en la teoría de la **Resiliencia Latente**, la cual postula que ciertos activos urbanos poseen una inteligencia espacial intrínseca debido a su consolidación histórica. Los santuarios y templos religiosos, emplazados estratégicamente en las zonas altas desde hace siglos, operan bajo esta lógica.
Dentro del motor algorítmico, estas geometrías se integran al grafo como un nuevo clúster de nodos de destino. El motor recalcula la matriz de accesibilidad exclusivamente para los nodos que habían colapsado en el paso anterior. Si el algoritmo halla una ruta de esfuerzo viable hacia estos recintos, el nodo es recodificado como "Rescatado". Esto permite calcular la **Capacidad de Absorción**, una métrica que cuantifica matemáticamente la proporción de la fractura territorial que es contenida y mitigada por el patrimonio histórico convertido en infraestructura de emergencia.

---

# Theoretical Framework and Analytical Foundations

This project employs the *Network Fracture Engine*, which is defined as an algorithmic engine designed to audit territorial resilience and simulate the degradation of mobility networks in the face of natural disasters (tsunamis). Its operation is not random; it is based on consolidated theories from various fields of urban theory, Disaster Risk Reduction (DRR), and quantitative geography. Likewise, it integrates methodologies from complex analytical disciplines—such as three-dimensional topological modeling and spatial vector calculus—to approach and decode the systemic vulnerability of the urban territory.

Below are the theories that nourish the algorithm's operation:

**1. Urban Topology and Graph Theory (Graph Theory vs. Space Syntax)**
To model evacuation infrastructure, the model discards flat Euclidean proximity and the traditional foundations of Space Syntax. While Space Syntax is optimal for predicting organic pedestrian flows under "normal" conditions based on visibility and urban integration, a disaster evacuation demands calculating forced flows under absolute physical stress. Therefore, the engine is built on **Graph Theory**. In the model, the road network is mathematically reconstructed as a directed topological graph $G = (V, E)$, where intersections are vertices ($V$) and street segments are edges ($E$). This allows the algorithm to evaluate the city as a structural network, where the physical loss of an edge alters the connectivity and operational cost of the entire system.

**2. Spatial Friction and Pedestrian Effort (Tobler's Hiking Function)**
To model pedestrian movement towards shelters, the algorithm rejects conventional "circular buffers", since applying linear radii in Kamakura's rugged topography results in a misleading interpretation of risk. Therefore, the algorithm applies the concept of **Spatial Friction**. Using local Digital Elevation Models (DEM), the engine injects the altimetric elevation ($Z$) into each graph node to calculate the slope of each street. Subsequently, it applies **Tobler's Hiking Function**, an empirical equation that penalizes the movement effort based on inclination. The algorithm translates 3D geometry into a travel time coefficient ($T$), mathematically penalizing steep hillsides and demonstrating that a visually nearby shelter can be operationally inaccessible due to orographic friction.

**3. Systemic Vulnerability and Minimum Cost Routing (Dijkstra's Algorithm)**
To integrate risk variables and evaluate the operational limit of civil protection, the model employs parametric stress simulations (10m, 20m, 30m of flooding). During the simulation, the code evaluates the minimum elevation of each road edge ($Z_{\text{min}}$); if the water level exceeds this elevation, the edge is removed from the graph, simulating the physical loss of the path.
On this fractured network, the algorithm executes accessibility calculations using **Dijkstra's Algorithm**, seeking the path of least effort cost (based on Tobler) from each point to the official State shelters. If the resulting vector towards the government network yields an infinite cost ($d \to \infty$), the engine penalizes the node, categorizing it as an "Isolated Node", thereby revealing the actual coverage deficit of public policy.

**4. Latent Resilience and Emergent Infrastructure**
The validation of the project's central hypothesis is based on the theory of **Latent Resilience**, which postulates that certain urban assets possess intrinsic spatial intelligence due to their historical consolidation. Shrines and religious temples, strategically located in high areas for centuries, operate under this logic.
Within the algorithmic engine, these geometries are integrated into the graph as a new cluster of destination nodes. The engine recalculates the accessibility matrix exclusively for the nodes that had collapsed in the previous step. If the algorithm finds a viable effort path to these sites, the node is recoded as "Rescued." This allows calculating the **Absorption Capacity**, a metric that mathematically quantifies the proportion of the territorial fracture that is contained and mitigated by historical heritage turned into emergency infrastructure.

---

Creo que ahora sí el documento respira exactamente la misma vibra, profundidad y estructura de Chongqing. Dime si le damos el visto bueno para cerrar con el Glosario.