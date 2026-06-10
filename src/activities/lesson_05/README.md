# applied_bigdata
Applied Big Data (Máster IA &amp; Big data, Linkiafp.es)

# Informe de Proyecto KDD: Análisis de Datos de Ventas de Amazon
**Fase de Minería de Datos y Estrategia Comercial**

**Autor:** David Cueli Chavarría  
**Entorno:** Máster FP IA & Big Data | Big Data Aplicado  

---

## ÍNDICE
1. [Contexto](#contexto)
2. [EJERCICIO 1](#ejercicio-1)
   - [Proyecto KDD](#proyecto-kdd)
3. [Resumen ejecutivo](#resumen-ejecutivo)
4. [Objetivo del proyecto](#objetivo-del-proyecto)
5. [Contexto y alcance](#contexto-y-alcance)
6. [Metodología](#metodología)
   - [Infraestructura técnica](#infraestructura-técnica)
   - [Entorno de trabajo](#entorno-de-trabajo)
   - [Herramientas de análisis](#herramientas-de-análisis)
7. [Datos utilizados y calidad](#datos-utilizados-y-calidad)
   - [Limpieza de datos](#limpieza-de-datos)
   - [Auditando Categorías (columna category)](#auditando-categorías-columna-category)
   - [Análisis y hallazgos](#análisis-y-hallazgos)
   - [Auditoría de Calidad y Consistencia del Dataset](#auditoría-de-calidad-y-consistencia-del-dataset)
   - [Trazabilidad de Reseña Única (user_id + review_id + product_id)](#trazabilidad-de-reseña-única-user_id--review_id--product_id)
     - [Depuración de duplicados relacionales](#depuración-de-duplicados-relacionales)
     - [Verificación de duplicados relacionales](#verificación-de-duplicados-relacionales)
   - [Auditoría de datos Null](#auditoría-de-datos-null)
8. [Minería de datos](#minería-de-datos)
   - [Estructura de Catálogo de Precios](#estructura-de-catálogo-de-precios)
   - [El Núcleo del Catálogo, el consumo masivo](#el-núcleo-del-catálogo-el-consumo-masivo)
   - [Naturaleza de los Casos atípicos coherentes](#naturaleza-de-los-casos-atípicos-coherentes)
   - [Conclusiones](#conclusiones)
9. [Recomendaciones](#recomendaciones)
   - [Auditoría de Popularidad para la Asignación de Presupuesto (Evitar Falsos Éxitos)](#auditoría-de-popularidad-para-la-asignación-de-presupuesto-evitar-falsos-éxitos)
   - [Estrategia de Venta Cruzada para el Núcleo del Catálogo (Consumo Masivo)](#estrategia-de-venta-cruzada-para-el-núcleo-del-catálogo-consumo-masivo)
   - [Segmentación de Alta Tecnología para los Casos Atípicos Coherentes (Gama Alta)](#segmentación-de-alta-tecnología-para-los-casos-atípicos-coherentes-gama-alta)
10. [Limitaciones](#limitaciones)
    - [Calidad del texto en las reseñas](#calidad-del-texto-en-las-reseñas)
    - [Ausencia de datos temporales o de coste](#ausencia-de-datos-temporales-o-de-coste)
11. [Conclusiones](#conclusiones-1)
    - [Importancia de la auditoría de datos](#importancia-de-la-auditoría-de-datos)
    - [Validación del enfoque cuantitativo](#validación-del-enfoque-cuantitativo)
    - [Realidad del inventario analizado](#realidad-del-inventario-analizado)
12. [Anexo](#anexo)

---

## Contexto
El presente documento constituye la entrega correspondiente al bloque práctico de minería de datos, enfocado en el procesamiento, auditoría y análisis de un catálogo de transacciones y valoraciones dentro de la plataforma Amazon.

## EJERCICIO 1
### Proyecto KDD
Se aplica la metodología estándar de Descubrimiento de Conocimiento en Bases de Datos (KDD) estructurada en las fases de selección, limpieza, transformación, minería de datos e interpretación de resultados.

## Resumen ejecutivo
Este informe detalla la auditoría técnica y el análisis estratégico del dataset de ventas de Amazon. Los resultados finales revelan una extrema polarización del catálogo, concentrando más del 97% de las referencias en apenas tres categorías principales (*Electronics*, *Computers&Accessories* y *Home&Kitchen*), dominadas por artículos económicos de consumo masivo. Asimismo, la auditoría de calidad destapó severas deficiencias estructurales en el empaquetado del archivo original, identificando fallos de extracción (*scraping*) que duplicaron observaciones de forma artificial al expandir los registros relacionales, y confirmando la total ausencia de variables temporales, lo que descarta metodológicamente cualquier análisis de estacionalidad en este catálogo.

## Objetivo del proyecto
El objetivo principal consiste en transformar un conjunto de datos en bruto (*raw data*) con deficiencias de estructura y consistencia en un repositorio limpio y optimizado, capaz de fundamentar decisiones estratégicas de negocio y reglas de asociación comerciales fiables.

## Contexto y alcance
El alcance del trabajo se centra en el análisis exploratorio y la ingeniería de características de un dataset realista de valoraciones de productos de Amazon India. El estudio abarca desde la detección de anomalías lógicas de extracción hasta la propuesta de segmentación de inventario para la asignación eficiente de presupuestos de marketing.

## Metodología
### Infraestructura técnica
El procesamiento se ejecuta de manera local sobre hardware dedicado, asegurando la persistencia y aislamiento de los entornos de ejecución mediante contenedores y sistemas de gestión de librerías estables.

### Entorno de trabajo
Se utiliza la suite integrada de desarrollo basada en cuadernos interactivos de Python, permitiendo una trazabilidad modular paso a paso de cada transformación aplicada sobre el DataFrame original.

### Herramientas de análisis
La pila tecnológica principal está compuesta por:
- **Pandas**: Para la ingesta, manipulación, limpieza y pivoteo de estructuras de datos tabulares.
- **Matplotlib & Seaborn**: Para la generación de la documentación gráfica y la auditoría visual de distribuciones estadísticas.

## Datos utilizados y calidad
### Limpieza de datos
La fase inicial requirió la normalización del formato regional (uso de rupias indias - INR), la eliminación de caracteres especiales en las cadenas numéricas de precio y la conversión estricta de tipos de datos de tipo objeto (*strings*) a coma flotante de precisión simple o doble.

### Auditando Categorías (columna category)
La variable original `category` presentaba una estructura jerárquica compactada en una única cadena de texto delimitada por caracteres "|". Se implementó un algoritmo de extracción de la categoría raíz mediante operaciones vectorizadas de cadenas de texto en Pandas.

El volumen limpio de categorías raíz únicas se redujo a 9 departamentos principales. Para asegurar la fidelidad estadística y evitar sesgos de popularidad provocados por la posterior expansión relacional del catálogo, el conteo descriptivo de inventario se restringe mediante la eliminación estricta de duplicados por identificador de producto:

### Análisis y hallazgos
La distribución real del inventario muestra una concentración asimétrica severa. Tres categorías acaparan casi la totalidad de las referencias físicas del catálogo: Electronics, Computers&Accessories y Home&Kitchen, mientras que los departamentos restantes (como OfficeProducts o MusicalInstruments) presentan una representación residual.

#### Auditoría de Calidad y Consistencia del Dataset
Mediante una inspección visual y analítica preliminar, se determinó que el conjunto de datos exhibe anomalías derivadas de un proceso de captura (scraping) defectuoso. La granularidad original mezcla registros de producto únicos con campos compuestos que incrustan listas de usuarios y reseñas en celdas individuales de texto plano.

#### Trazabilidad de Reseña Única (user_id + review_id + product_id)
Al ejecutar funciones de separación de listas mediante el método .explode(), el volumen formal de filas se expande artificialmente de 1.465 registros originales a 11.503 observaciones. Esta multiplicación no representa un crecimiento del catálogo de productos, sino la desagregación de las interacciones históricas de los usuarios por cada referencia.

  - <b>Depuración de duplicados relacionales</b><br>
    Se detectaron duplicaciones lógicas severas. Casos específicos demuestran que el script original insertó cadenas idénticas repetidas de identificadores en una misma celda, provocando que la función de expansión generase registros idénticos correlativos para el mismo producto y el mismo usuario.

  - <b>Verificación de duplicados relacionales</b><br>
    Se implementaron restricciones booleanas mediante .duplicated() combinando las claves primarias relacionales ['product_id', 'user_id'] para aislar y purgar el ruido analítico introducido por la herramienta de extracción.

### Auditoría de datos Null
El volumen de valores ausentes (NaN) se localizó exclusivamente en las variables críticas de valoración (rating_count). Al representar una proporción inferior al 1% de la muestra total del inventario, se determinó su exclusión directa mediante .dropna() sin aplicar métodos de imputación artificial que pudiesen sesgar las métricas de desviación estándar de los precios.

## Minería de datos
### Estructura de Catálogo de Precios
La distribución de precios reales (actual_price) y precios promocionales (discounted_price) muestra un comportamiento asimétrico positivo con una alta concentración en el extremo inferior de la escala económica. La variabilidad se analiza formalmente mediante la implementación opcional de visualizaciones de escala logarítmica para mitigar el efecto de dispersión visual de los productos de alta gama.

### El Núcleo del Catálogo, el consumo masivo
La analítica cuantitativa confirma que el volumen transaccional de la plataforma se sostiene sobre un núcleo denso de productos de bajo precio unitario. Artículos de conectividad, cables y accesorios periféricos representan la base operativa del negocio en términos de rotación.

### Naturaleza de los Casos atípicos coherentes
Los valores atípicos (outliers) identificados en los diagramas de caja e histogramas no corresponden a errores tipográficos ni a fallos de carga de datos. Son registros coherentes correspondientes a bienes tecnológicos de alto coste unitario (computadores portátiles y televisores inteligentes).

### Conclusiones
Existe una división estructural nítida en los datos: un ecosistema de alta frecuencia y bajo margen (accesorios) frente a un ecosistema de baja frecuencia y alto coste (dispositivos de gama alta).

## Recomendaciones
### Auditoría de Popularidad para la Asignación de Presupuesto (Evitar Falsos Éxitos)
  <b>Acción de negocio</b><br>

    Restringir la evaluación de rendimiento de producto basada únicamente en el volumen bruto de comentarios o filas duplicadas tras el explode.

    Evita la asignación errónea de presupuestos publicitarios hacia productos cuya popularidad aparente está inflada por el ruido relacional del dataset estructurado.

### Estrategia de Venta Cruzada para el Núcleo del Catálogo (Consumo Masivo)
  <b>Acción de negocio</b><br>

    Diseñar paquetes de productos indexados (bundles) que vinculen los accesorios de alta rotación directamente con las categorías complementarias mayoritarias.

    Maximiza el valor medio del ticket de compra (AOV) aprovechando la tracción natural de las tres categorías raíz dominantes.

### Segmentación de Alta Tecnología para los Casos Atípicos Coherentes (Gama Alta)
  <b>Acción de negocio</b><br>

    Aislar del catálogo general las referencias identificadas estadísticamente como outliers de precio dentro de Computers y Electronics para someterlas a campañas exclusivas basadas en especificaciones técnicas y opciones de financiación.

    Optimiza el coste de adquisición de clientes (CAC) al evitar la dilución del margen publicitario en audiencias masivas no calificadas.

## Limitaciones
### Calidad del texto en las reseñas
Las columnas de texto libre presentan problemas de codificación y delimitación por comas internas que corrompen la estructura tabular tradicional, impidiendo la aplicación inmediata de algoritmos estables de procesamiento de lenguaje natural (NLP) sin una fase previa de re-tokenización.

### Ausencia de datos temporales o de coste
El conjunto de datos carece de marcas de tiempo (timestamps), fechas de compra o registros de costes logísticos. Esta omisión invalida cualquier intento metodológico de proyección de demanda, análisis de series temporales o cálculo directo del margen de beneficio neto del catálogo.

## Conclusiones
### Importancia de la auditoría de datos
La fase de auditoría técnica demostró ser un paso obligatorio previo al modelado. Confiar en los volúmenes brutos de la extracción original habría conducido a conclusiones comerciales sesgadas y falsos éxitos de venta.

### Validación del enfoque cuantitativo
La consistencia interna de las variables numéricas de precio y puntuación justifica la validez de los modelos descriptivos construidos, aislando el valor del informe en métricas estadísticas estables.

### Realidad del inventario analizado
El inventario analizado refleja una plataforma comercial altamente especializada en la provisión masiva de componentes electrónicos de bajo coste, con incursiones puntuales de alto valor que requieren tratamientos analíticos independientes.

## Anexo
El código fuente parametrizado, las funciones dinámicas de visualización (<i>PlotPriceDistribution</i>, <i>PlotCategoryDistribution</i>, <i>PlotPriceByCategory</i>) y los cuadernos de ejecución limpia se encuentran disponibles en el repositorio de control de versiones del proyecto.