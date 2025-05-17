#  Machine Learning Operations (MLOps)

---
## Caso de estudio

### Antecedentes

La explosión de datos en la medicina moderna ha transformado la forma en que entendemos y abordamos la salud. Los registros electrónicos de salud, los dispositivos portátiles generan una cantidad ingente de información sobre los pacientes. Esta riqueza de datos ha impulsado avances significativos en el desarrollo de modelos de aprendizaje automático capaces de predecir enfermedades comunes con una precisión cada vez mayor. Sin embargo, este panorama prometedor se ve desafiado cuando nos enfrentamos a las enfermedades raras o huérfanas. Estas condiciones, que afectan a un número reducido de individuos, se caracterizan precisamente por la escasez de datos disponibles. La falta de suficientes ejemplos dificulta enormemente la aplicación de técnicas tradicionales de aprendizaje automático, que suelen requerir grandes conjuntos de datos para un entrenamiento efectivo. Por lo tanto, el reto radica en desarrollar metodologías innovadoras que puedan construir modelos predictivos robustos incluso con información limitada, cerrando la brecha entre la abundancia de datos para enfermedades comunes y la escasez para las enfermedades huérfanas, con el fin último de mejorar el diagnóstico y la atención de todos los pacientes. 

---

## Definición del problema

Dados los avances tecnológicos, en el campo de la medicina la cantidad de información que existe de los pacientes es muy abundante. Sin embargo, para algunas enfermedades no tan comunes, llamadas huérfanas, los datos que existen escasean. Se requiere construir un modelo que sea capaz de predecir, dados los datos de síntomas de un paciente, si es posible o no que este sufra de alguna enfermedad. Esto se requiere tanto para enfermedades comunes (muchos datos) como para enfermedades huérfanas (pocos datos). 


### Guía de Configuración 

Este proyecto consta de un formulario o aplicación frontend y backend, contenerizadas usando Docker y orquestadas con Docker Compose. El frontend es un archivo HTML estático (`index.html`) servido por Nginx en el puerto 8000, y el backend es una aplicación FastAPI (`application.py`) ejecutándose en el puerto 5000. Este README proporciona instrucciones detalladas para construir y ejecutar cada componente individualmente usando `Dockerfile.frontend` y `Dockerfile.backend`, así como juntos usando `docker-compose.yml`.

## Estructura del Proyecto

```
your_project/
├── Dockerfile.frontend      # Dockerfile para el frontend (Nginx)
├── Dockerfile.backend       # Dockerfile para el backend (FastAPI)
├── docker-compose.yml       # Configuración de Docker Compose para ambos servicios
├── nginx.conf               # Configuración de Nginx para el frontend
├── model/
│   ├── prediction/
│   │   └── application.py   # Aplicación backend FastAPI
│   ├── frontend/
│   │   └── index.html       # Archivo HTML estático del frontend
```

## Requisitos Previos

Antes de continuar, asegúrate de tener instalados los siguientes elementos en tu sistema:

- **Docker**: Versión 20.10 o superior. Instala desde [el sitio oficial de Docker](https://docs.docker.com/get-docker/).
- **Docker Compose**: Versión 2.0 o superior. Normalmente incluido con Docker Desktop, o instálalo por separado siguiendo la [guía de instalación de Docker Compose](https://docs.docker.com/compose/install/).
- **Git** (opcional): Para clonar el repositorio, si aplica.
- **Python 3.9+** (opcional): Solo necesario si deseas inspeccionar o modificar `application.py` localmente.
- Una terminal o interfaz de línea de comandos.

- El backend (`application.py`) es una aplicación FastAPI con una variable `app` definida (por ejemplo, `app = FastAPI()`).
- Existe un archivo `requirements.txt` en `model/prediction/` con dependencias como `fastapi==0.115.0` y `uvicorn==0.30.6`.
- El frontend (`index.html`) es un archivo estático servido por Nginx.
- El sistema tiene acceso a los puertos 8000 (frontend) y 5000 (backend). Si estos puertos están en uso, ajusta los mapeos de puertos en `docker-compose.yml` o detén los servicios en conflicto.

---

![ML Pipeline](./imgs/MLOPsv2.png)
---
## Caso de estudio

### Antecedentes

La explosión de datos en la medicina moderna ha transformado la forma en que entendemos y abordamos la salud. Los registros electrónicos de salud, los dispositivos portátiles generan una cantidad ingente de información sobre los pacientes. Esta riqueza de datos ha impulsado avances significativos en el desarrollo de modelos de aprendizaje automático capaces de predecir enfermedades comunes con una precisión cada vez mayor. Sin embargo, este panorama prometedor se ve desafiado cuando nos enfrentamos a las enfermedades raras o huérfanas. Estas condiciones, que afectan a un número reducido de individuos, se caracterizan precisamente por la escasez de datos disponibles. La falta de suficientes ejemplos dificulta enormemente la aplicación de técnicas tradicionales de aprendizaje automático, que suelen requerir grandes conjuntos de datos para un entrenamiento efectivo. Por lo tanto, el reto radica en desarrollar metodologías innovadoras que puedan construir modelos predictivos robustos incluso con información limitada, cerrando la brecha entre la abundancia de datos para enfermedades comunes y la escasez para las enfermedades huérfanas, con el fin último de mejorar el diagnóstico y la atención de todos los pacientes. 

---

## Definición del problema

Dados los avances tecnológicos, en el campo de la medicina la cantidad de información que existe de los pacientes es muy abundante. Sin embargo, para algunas enfermedades no tan comunes, llamadas huérfanas, los datos que existen escasean. Se requiere construir un modelo que sea capaz de predecir, dados los datos de síntomas de un paciente, si es posible o no que este sufra de alguna enfermedad. Esto se requiere tanto para enfermedades comunes (muchos datos) como para enfermedades huérfanas (pocos datos). 

### Origenes de datos

Data Source es un componente fundamental que representa el origen y la infraestructura de almacenamiento de los datos utilizados a lo largo de la pipeline de MLOps. En el contexto de este caso de estudio, la fuente principal es el "Conjunto de Datos de Pacientes: Datos Demográficos y Clínicos". Este conjunto de datos es una recopilación detallada de información de personas diagnosticadas con enfermedades comunes y raras, incluyendo tanto datos demográficos (edad, género, etc.) como información clínica (fecha de diagnóstico, duración de síntomas, diagnósticos previos).
Los datos provienen de orígenes públicos y privados, e incluyen archivos no estructurados, como registros de historias clínicas, así como datos que pueden ser representados en tablas o bases de datos estructuradas.
Para gestionar esta diversidad de datos desde su origen dentro del entorno de Azure, se utilizan varias tecnologías clave:
    • Los archivos no estructurados provenientes de fuentes públicas y privadas se almacenan inicialmente en Azure Blob Storage. Este servicio es ideal para manejar millones de archivos con escalabilidad y facilidad de acceso. El almacenamiento en Blob Storage actúa como un Data Lake para estos datos brutos.
    • Después del preprocesamiento necesario para normalizar y limpiar los datos, la información transformada y estructurada se almacena en Azure Synapse Analytics. Este componente funciona como un Data Warehouse, ofreciendo una integración nativa con Azure Blob Storage y capacidades avanzadas para consultas eficientes.
    • Las fuentes de datos pueden ser accedidas a través de API connectors.
El acceso a estos datos es el punto de partida para la extracción de datos e inicia el proceso de la pipeline, incluyendo la validación y preparación. La disponibilidad de nuevos datos en el Data Source es un disparador clave para el reentrenamiento automático del modelo (Continuous Training), asegurando que el modelo se mantenga actualizado y evitando su degradación debido a cambios en la distribución de los datos. La validación de datos y el versionamiento de los conjuntos de datos son principios importantes aplicados a la Data Source para asegurar la calidad y reproducibilidad del proceso.

### Almacenamiento y Esquema de datos

"Data Schema and Storage" en la pipeline de MLOps representa la infraestructura y organización de los datos utilizados para el caso de estudio de predicción de enfermedades. Este componente es crucial ya que define dónde y cómo se almacenan los datos, y cómo se asegura su calidad y estructura inicial antes de ser procesados para el entrenamiento del modelo.
Las fuentes de datos provienen de orígenes públicos y privados, e incluyen tanto registros médicos no estructurados como datos que pueden presentarse en bases de datos estructuradas o tablas. Para manejar esta diversidad, los archivos no estructurados, como historias clínicas y datos demográficos brutos de diversas fuentes, se almacenan en Azure Blob Storage. Este servicio actúa como un Data Lake, permitiendo almacenar millones de archivos con escalabilidad y rápida recuperación. Estos datos requieren un preprocesamiento para normalizar formatos y limpiar la información. Posteriormente, los datos transformados y estructurados se almacenan en Azure Synapse Analytics. Azure Synapse funciona como un Data Warehouse, ofreciendo integración nativa con Azure Blob Storage y capacidades avanzadas para consultas SQL eficientes, lo cual es ideal para preparar los conjuntos de datos para el entrenamiento de modelos de Machine Learning.
El concepto de "Data Schema" aquí se refiere a la definición y validación de la estructura y el dominio de los datos. Esto es una parte fundamental de la validación de datos, donde se calculan estadísticas y se define un esquema para los datos de entrada. Asegurar un esquema consistente es vital para la calidad del entrenamiento y para monitorear la calidad de los datos y evitar desviaciones en producción.

Data Cleaning (Limpieza de Datos) es fundamental y se aplica después de la ingesta inicial. Su objetivo es abordar elementos críticos como campos faltantes, archivos corruptos, incompatibilidades de tipo y la detección y tratamiento de casos atípicos inesperados. Este paso garantiza la calidad y consistencia de los datos brutos provenientes de diversas fuentes públicas y privadas.
Una vez que los datos están limpios y preparados, se inicia la fase de ingeniería de características. Esto incluye procesos como el Análisis de Componentes Principales (PCA), que se utiliza para reducir la dimensionalidad del conjunto de datos conservando la mayor parte de la información relevante, mejorando la eficiencia computacional. La extracción de características identifica variables críticas, mientras que las agregaciones consolidan los datos en resúmenes significativos. La selección de características se encarga de definir el conjunto final de variables que se utilizarán para entrenar el modelo.
Para gestionar de manera eficiente estas características procesadas, se utiliza un Feature Store. Este repositorio es esencial para reutilizar características en múltiples modelos y proyectos, evitando la duplicación de esfuerzos en la ingeniería de características. También ayuda a deacoplar el proceso de ingeniería de características del entrenamiento y la inferencia, asegurando la consistencia entre el entrenamiento y el servicio del modelo. Los Data Scientists pueden acceder al Feature Store para encontrar características existentes o agregar nuevas características procesadas. En una arquitectura MLOps avanzada, el Feature Store se convierte en el punto de acceso principal para los datos de características, en lugar de conectarse directamente a los data warehouses o fuentes de datos originales.
Para implementar estos procesos en Azure, se pueden utilizar varias tecnologías. Azure Synapse Analytics y Azure Databricks con Spark son plataformas adecuadas para realizar el preprocesamiento, la limpieza de datos, la ingeniería de características y el análisis exploratorio de datos a escala, especialmente con grandes volúmenes de datos. El Feature Store en Azure se puede implementar utilizando una combinación de servicios de almacenamiento y procesamiento, y Azure Machine Learning ofrece funcionalidades de Feature Store. Herramientas de Python como Pandas y NumPy son comúnmente utilizadas en la limpieza y procesamiento de datos, y scikit-learn para PCA y selección de características, a menudo ejecutadas en entornos como Azure Databricks o Azure ML Compute instances. [link](https://pycaret.gitbook.io/docs) PyCaret, como contenedor de estas bibliotecas, puede simplificar y automatizar muchas de estas tareas de preprocesamiento y experimentación

---
## Iteraciones del modelo

### Proceso de ingeniería de caracteristicas

Data Cleaning (Limpieza de Datos) es fundamental y se aplica después de la ingesta inicial. Su objetivo es abordar elementos críticos como campos faltantes, archivos corruptos, incompatibilidades de tipo y la detección y tratamiento de casos atípicos inesperados. Este paso garantiza la calidad y consistencia de los datos brutos provenientes de diversas fuentes públicas y privadas.
Una vez que los datos están limpios y preparados, se inicia la fase de ingeniería de características. Esto incluye procesos como el Análisis de Componentes Principales (PCA), que se utiliza para reducir la dimensionalidad del conjunto de datos conservando la mayor parte de la información relevante, mejorando la eficiencia computacional. La extracción de características identifica variables críticas, mientras que las agregaciones consolidan los datos en resúmenes significativos. La selección de características se encarga de definir el conjunto final de variables que se utilizarán para entrenar el modelo.
Para gestionar de manera eficiente estas características procesadas, se utiliza un Feature Store. Este repositorio es esencial para reutilizar características en múltiples modelos y proyectos, evitando la duplicación de esfuerzos en la ingeniería de características. También ayuda a deacoplar el proceso de ingeniería de características del entrenamiento y la inferencia, asegurando la consistencia entre el entrenamiento y el servicio del modelo. Los Data Scientists pueden acceder al Feature Store para encontrar características existentes o agregar nuevas características procesadas. 
En una arquitectura MLOps avanzada, el Feature Store se convierte en el punto de acceso principal para los datos de características, en lugar de conectarse directamente a los data warehouses o fuentes de datos originales.
Para implementar estos procesos en Azure, se pueden utilizar varias tecnologías. Azure Synapse Analytics y Azure Databricks con Spark son plataformas adecuadas para realizar el preprocesamiento, la limpieza de datos, la ingeniería de características y el análisis exploratorio de datos a escala, especialmente con grandes volúmenes de datos. El Feature Store en Azure se puede implementar utilizando una combinación de servicios de almacenamiento y procesamiento, y Azure Machine Learning ofrece funcionalidades de Feature Store. Herramientas de Python como Pandas y NumPy son comúnmente utilizadas en la limpieza y procesamiento de datos, y scikit-learn para PCA y selección de características, a menudo ejecutadas en entornos como Azure Databricks o Azure ML Compute instances.[link](https://pycaret.gitbook.io/docs)  PyCaret, como contenedor de estas bibliotecas, puede simplificar y automatizar muchas de estas tareas de preprocesamiento.

### Experimentos orquestados

1. Data Validation: Este proceso es fundamental para asegurar la calidad de los datos de entrada. Implica verificar automáticamente el esquema y el dominio de los datos y las características, calculando estadísticas a partir de los datos de entrenamiento para definir expectativas. Es vital para detectar errores tempranamente y asegurar que los datos coincidan con la estructura esperada. Las tecnologías de Azure como Azure Synapse Analytics y Azure Databricks pueden utilizarse para realizar estas verificaciones a escala, a menudo implementadas con bibliotecas como Pandas y Numpy.
2. Data Preparation: Esta etapa se enfoca en limpiar y transformar los datos validados para hacerlos adecuados para el entrenamiento del modelo. Incluye la limpieza de datos (manejo de valores faltantes, corrección de errores), análisis exploratorio de datos (EDA) para comprender las características, y transformaciones necesarias. Este proceso alimenta la pipeline de ingeniería de características. Plataformas como Azure Synapse Analytics y Azure Databricks con Apache Spark son ideales para ejecutar estas tareas de procesamiento de datos a gran escala.
3. Model Training: Aquí se desarrollan los algoritmos predictivos utilizando los datos preparados. Implica la experimentación con diferentes modelos y la optimización de sus parámetros. El objetivo es obtener un modelo con calidad estable. Se utilizan bibliotecas como scikit-learn y [link](https://pycaret.gitbook.io/docs) PyCaret, a menudo ejecutadas en entornos de computación escalables de Azure. El entrenamiento debe ser reproducible y puede ser parte de una pipeline automatizada disparada por nuevos datos.
4. Model Evaluation: Una vez entrenados, los modelos se evalúan para medir su rendimiento. Para tareas de clasificación, se revisan métricas como ROC AUC, F1-score, accuracy, y la Confusion matrix. También se considera la complejidad del modelo y los tiempos de inferencia. Se utiliza validación cruzada para probar el modelo con diferentes subconjuntos de datos. Los resultados se registran y pueden visualizarse en paneles (por ejemplo, con Matplotlib + MLflow) para la toma de decisiones.
5. Model Validation: Este es un paso crítico para decidir si el modelo entrenado está listo para ser desplegado en producción. Se realiza una evaluación exhaustiva para verificar si el modelo cumple con los criterios mínimos de calidad (accuracy, rendimiento, etc.) definidos previamente. Si el modelo satisface estos umbrales, avanza al despliegue; de lo contrario, se regresa a las fases anteriores (iteración, entrenamiento). Esta validación incluye probar la posible degradación del modelo en un conjunto de validación y verificar la consistencia entre el entorno de entrenamiento y servicio.
Estos procesos se integran en una pipeline automatizada, donde la validación de datos y modelos, así como el entrenamiento, pueden ser disparados automáticamente, asegurando la calidad y eficiencia en el ciclo de vida del MLOps.

#### Selección y evaluación del modelo

Comparación, Selección y Evaluación de Modelos son etapas críticas después del entrenamiento iterativo.
Tras realizar múltiples Iteraciones del Modelo, que implican la experimentación con diferentes algoritmos y la optimización de parámetros, se procede a la Comparación entre modelos. Esta fase implica evaluar los candidatos entrenados basándose en métricas importantes para la clasificación, como ROC AUC,  F1-score, accuracy, y la Confusion matrix. También se consideran aspectos como la complejidad computacional (temporal y espacial) y los tiempos de inferencia. La validación cruzada k-fold se utiliza para probar los modelos con diversos subconjuntos de datos. Herramientas como [link](https://pycaret.gitbook.io/docs) PyCaret facilitan este proceso de comparación, y MLflow junto con Matplotlib pueden utilizarse para registrar y visualizar los resultados de estas comparaciones.
Una vez realizada la comparación, se procede a la Selección del mejor modelo según los requisitos. Esta selección se fundamenta en el análisis comparativo y debe alinearse con los criterios predefinidos, que pueden incluir requisitos de negocio, recursos, tiempos de inferencia y facilidad de uso.
El modelo seleccionado pasa por una Evaluación del modelo seleccionado, también llamada Model Validation. Este es un paso crucial para determinar si el modelo cumple con los criterios mínimos de calidad necesarios para ser implementado en producción. Se verifica si el modelo satisface los umbrales establecidos en cuanto a accuracy y rendimiento. Si no los cumple, el proceso regresa a la fase de iteración y experimentación.
Durante estas fases, se generan Model performance metrics & dashboards. Las métricas de rendimiento se registran y visualizan, a menudo utilizando herramientas como MLflow y Matplotlib, o potencialmente Tableau, para fundamentar la decisión de selección y presentarla a las partes interesadas. Estas métricas son esenciales para el Monitoreo del Modelo en producción, donde se verifica la calidad y se detectan problemas como la degradación del modelo y los cambios en la distribución de datos (drift). Azure Monitor es una tecnología de Azure recomendada para el monitoreo del rendimiento del modelo en producción.
Finalmente, después de la selección y validación, es fundamental Save model, params and artifacts. El modelo elegido, junto con sus parámetros y artefactos asociados, se serializa (por ejemplo, usando formatos como pickle o protobuf) y se guarda en un repositorio. 


Una vez finalizadas estas estapas del Pipelne de MLOPs es curcial establecer donde se versionan y almacenan los modelos y su metadata, asegurando la Reproducibilidad y auditabilidad del proceso. Esto se relaciona con el concepto de Model Registry y Experiment TrackingLas, las tecnologías de Azure, como Azure Machine Learning, ofrecen funcionalidades para el registro y versionamiento de modelos.

---

## Depliegue del modelo

Model Deployment (Implementación del Modelo) es una fase crítica y automatizada dentro de la pipeline de machine learning. Su objetivo principal es poner a disposición el modelo validado para que pueda ser consumido y generar predicciones en los entornos disponibles calidad, preproducción o producción.
Este proceso se ejecuta después de que el modelo ha pasado por las fases de iteraciones, selección, evaluación y, crucialmente, validación, asegurando que cumple con los criterios mínimos de calidad definidos. Según los principios de MLOps, la implementación debe ser un paso automatizado, a menudo integrado en una pipeline de CI/CD (Continuous Delivery).

### Proceso automatizado
Técnicamente, la implementación generalmente implica la serialización del modelo (por ejemplo, utilizando formatos como pickle o protobuf) y su exportación al entorno donde se realizarán las predicciones. Para el caso de estudio específico, que requiere el procesamiento de millones de archivos de datos de pacientes en una ventana de tiempo limitada, se necesitan capacidades de procesamiento de big data.
En este contexto, el modelo serializado se exporta a procesadores de big data como Azure HDInsight o Azure Databricks con Spark. Estas plataformas de Azure permiten aprovechar la potencia de clústeres multi-nodo con nodos de trabajo distribuidos para paralelizar eficientemente la carga de predicciones. Se configura un "job" o trabajo de predicción que, una vez activado, ejecuta el modelo sobre los datos. La activación puede ser externa, por ejemplo, a través de un script en PySpark. Una alternativa sugerida para la orquestación de la infraestructura es Azure Kubernetes Service (AKS), especialmente útil si hay diversas necesidades de infraestructura.
La arquitectura en Azure no solo proporciona la escalabilidad necesaria para el procesamiento intensivo, sino también integración con otros servicios y capacidades avanzadas de monitoreo a través de Azure Monitor. El resultado es un servicio de predicción (CD: Model Serving) diseñado para estar disponible de forma continua (24/7) y proporcionar predicciones en tiempo real bajo demanda. Las predicciones generadas pueden almacenarse de forma estructurada en Azure Storage. Este proceso es fundamental para que el modelo tenga un impacto real al ser utilizado por el personal médico para predecir la probabilidad de enfermedades.


###  Modelo como servicio

#### Predicciones del modelo
Una vez implementado en el entorno productivo, el sistema de predicción médica operará con disponibilidad ininterrumpida las veinticuatro horas del día, durante los siete días de la semana, garantizando acceso permanente para el personal médico. La arquitectura ha sido diseñada para proporcionar predicciones en tiempo real bajo demanda, respondiendo de manera inmediata a las solicitudes de los profesionales.
Las prediciones se almacenan de forma extructura en Storaga de Azure.

#### Monitoreo del Modelo
 
Monitoreo del Modelo es un proceso altamente recomendable y crítico que se lleva a cabo una vez que el modelo ha sido implementado en producción. Aunque inicialmente pueda no ser un requisito inmediato, es una fase estratégica para asegurar la calidad continua del sistema de predicción.
Este proceso implica la monitorización exhaustiva del modelo para identificar desviaciones, problemas de calidad de datos y degradación del rendimiento predictivo. Se enfoca en controlar el rendimiento del modelo en datos en vivo, verificando la calidad y detectando problemas como el data drift y la model degradation. Principios como el Continuous Monitoring (CM) se centran en monitorear las métricas de rendimiento del modelo en producción, las cuales están ligadas a métricas de negocio.

La implementación de una solución como Azure Monitor facilita la detección temprana de anomalías, permitiendo adoptar medidas correctivas proactivas antes de que los problemas afecten negativamente. El sistema puede configurarse para generar notificaciones automáticas cuando los indicadores de rendimiento se desvían de los parámetros esperados. El monitoreo continuo ayuda a identificar cuándo el modelo se vuelve stale (obsoleto) y a determinar con qué frecuencia debe reentrenarse. Se deben monitorear cambios en la distribución de los datos y si las características de entrenamiento y servicio computan el mismo valor.

Crucialmente, el monitoreo puede disparar el reentrenamiento del modelo. Si el sistema detecta una disminución significativa en el rendimiento o un drift de datos, puede trigger para ejecutar el pipeline o iniciar un nuevo ciclo de experimentación. Esto crea un ciclo automatizado que retorna a la etapa de iteración del modelo para reentrenarlo con datos actualizados y posteriormente volver a implementarlo. Herramientas como MLflow y Matplotlib pueden usarse para visualizar métricas de rendimiento en dashboards. El monitoreo es vital para mantener la calidad y fiabilidad del modelo en producción y asegurar que cumple su objetivo.
