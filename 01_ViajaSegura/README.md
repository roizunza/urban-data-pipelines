# Marco Teórico: Fundamentos de la Movilidad de Cuidados

El presente proyecto se fundamenta en la necesidad de decodificar la movilidad periférica desde una **perspectiva de género e interseccionalidad**. A diferencia de los modelos de transporte tradicionales enfocados en viajes pendulares (hogar-trabajo), este análisis utiliza herramientas de geointeligencia para medir la eficiencia de una ruta que sustenta la **economía de los cuidados**.

A continuación, se explican los pilares teóricos y analíticos que validan este modelo:

**1. Movilidad de Cuidados y Viajes Encadenados (Trip Chaining)**
El análisis se basa en el concepto de **Movilidad del Cuidado**, desarrollado por Inés Sánchez de Madariaga. Esta teoría identifica que las mujeres realizan patrones de viaje más complejos que los hombres, caracterizados por **viajes encadenados** (paradas breves y sucesivas para dejar niños en la escuela, ir al mercado o asistir a una clínica). Mientras que el transporte masivo está diseñado para la eficiencia radial, el servicio que presta la Asociación Civil **Ruta 66** actúa como un puente que une estos nodos. El modelo de datos diseñado captura esta dinámica al no solo contar pasajeras, sino relacionar los ascensos y descensos con el equipamiento urbano circundante relacionado al trabajo de cuidados.

**2. Urbanismo de Proximidad y la "Última Milla" en la Periferia**
En zonas de topografía accidentada y periferia alta, el concepto de la "Ciudad de los 15 minutos" se enfrenta a la barrera de la **fricción espacial**. El proyecto utiliza la teoría de la **Última Milla** para demostrar que, ante la ausencia de infraestructura pesada (Metro/Metrobús), el transporte concesionado es el único capaz de resolver la conectividad capilar. El algoritmo de análisis emplea **Isocronas de 500 metros** como métrica de accesibilidad peatonal real, validando que el servicio es eficiente si permite a la usuaria acceder a sus nodos de cuidado en una caminata menor a 10 minutos desde la parada.

**3. Sintaxis Urbana y Topografía Crítica**
La configuración morfológica del sur de la CDMX impone restricciones físicas que dictan la red de transporte. Utilizando fundamentos de **Sintaxis Espacial**, el proyecto entiende la ruta no solo como un trazo, sino como un eje de integración que conecta zonas aisladas con centros de intercambio modal regionales (como Ciudad Universitaria). La validación geoespacial realizada en **QGIS** permite demostrar que la flexibilidad de la ruta concesionada es una respuesta adaptativa a la topografía, donde la jerarquía vial se ve sustituida por la necesidad de cobertura social.

**4. Interseccionalidad y Justicia Espacial**
El proyecto incorpora la **Interseccionalidad** como variable analítica, reconociendo que las usuarias de la Ruta 66 no solo enfrentan brechas de género, sino también de clase y ubicación geográfica. La herramienta visibiliza esta labor de las asociaciones civiles, muchas veces invisibilizada en las métricas oficiales, como un ejercicio de **Justicia Espacial** (Edward Soja). Al mapear la demanda exclusiva, se está tangibilizando un derecho a la ciudad que el diseño urbano tradicional ha pasado por alto.

**5. Validación mediante Indicadores de Demanda y Proximidad**
Para otorgar rigor técnico a la propuesta ante SEMOVI, se utiliza un método de **Evaluación Espacial** que cruza:
*   **Densidad de Equipamiento:** Conteo de nodos de salud, educación y abasto en el área de influencia de cada parada.
*   **Métricas de Ocupación:** Análisis de ascensos y descensos para identificar "hotspots" de cuidado.
La correlación positiva entre alta demanda y alta densidad de equipamiento confirma empíricamente que la ruta es el soporte físico de la red de cuidados del territorio.
