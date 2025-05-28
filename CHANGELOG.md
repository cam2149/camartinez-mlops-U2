# MLOps CHANGELOG

---

## Cambios en el esquema de arquitectura
---
### Versión 1.0 (MLOPs)
- Implementación inicial del pipeline MLOps.
- **Entrada de Datos**: Integración de fuentes de datos (Registros de Archivos, Fuente de Datos Pública/Privada) con Esquema y Almacenamiento de Datos utilizando BlobStorage y Azure Synapse Analytics DatLake.
- **Entrenamiento Offline**: Introducción de EDA (unión de conjuntos de datos) y extracciones/agregaciones de características PCA utilizando pandas, NumPy, Jupyter y Learn.
- **Iteraciones del Modelo**: Incluyó entrenamiento de modelos, optimización y experimentación con PyCaret y GitHub GitHub Actions.
- **Selección y Evaluación del Modelo**: Agregó comparación entre modelos usando mlflow y matpllib, selección del mejor modelo según requisitos, y evaluación del modelo seleccionado con métricas de rendimiento y tableros.
- **Despliegue del Modelo**: Serialización del modelo (pickle, protobuf) y despliegue en clúster multinodo usando Azure Databricks y Spark.
- **Predicciones del Modelo**: Gestión de información de pacientes, realización de predicciones y guardado de predicciones en Azure Blob Storage.
- **Monitoreo**: Implementación de monitoreo de modelos con verificaciones de calidad de datos y degradación del modelo usando Jupyter, Azure Policy y Azure Monitor.

### Versión 2.0 (MLOPsv2)
- **Entrada de Datos**: Mejorada con conectores API y verificación de deriva de datos usando Dipper.
- **Pipeline de Ingeniería de Características**: Agregó limpieza de datos, selección de características PCA y almacén de características usando pandas, Featuretools y Feast.
- **Análisis de Datos**: Integración de validación y preparación de datos.
- **Iteraciones del Modelo**: Expandido con experimentos orquestados usando mlflow.
- **Selección y Evaluación del Modelo**: Mejorado con comparación detallada entre modelos y guardado de parámetros/artefactos del modelo.
- **Pipeline Automatizado**: Introdujo pasos de extracción, preparación de datos, entrenamiento de modelos, evaluación y validación.
- **Despliegue del Modelo**: Agregó CI/CD de servicio de modelos con servicio de predicción.
- **Monitoreo de Rendimiento**: Incluyó monitoreo de modelos para derivas de calidad y degradación de datos.
- **Repositorio de Código Fuente**: Integrado con Repositorio de Código Fuente para despliegue de pipeline.

### Versión 3.0 (MLOPsv3)
- **Entrada de Datos**: Mantenido Esquema y Almacenamiento de Datos con BlobStorage y Azure Synapse Analytics DatLake.
- **Pipeline de Ingeniería de Características**: Mantenida limpieza de datos, selección de características PCA y almacén de características con pandas, Featuretools y Feast.
- **Análisis de Datos**: Mantenida validación y preparación de datos.
- **Iteraciones del Modelo**: Mejorado con experimentos orquestados y entrenamiento de modelos, optimización y experimentación.
- **Selección y Evaluación del Modelo**: Mantenida comparación entre modelos, selección del mejor modelo y evaluación con métricas de rendimiento y tableros.
- **Pipeline Automatizado**: Mantenidos pasos de extracción, preparación de datos, entrenamiento de modelos, evaluación y validación.
- **Despliegue del Modelo**: Mejorado con preparación de trabajo para realizar predicciones y despliegue de aplicaciones usando Docker.
- **Predicciones del Modelo**: Mejorado flujo de gestión de información de pacientes y realización de predicciones.
- **Monitoreo**: Actualizado monitoreo de modelos con verificaciones de derivas de calidad, degradación de datos e integración con Azure Databricks, Jupyter, Azure Policy y Azure Monitor.
- **Suscripción de Cliente**: Agregado CD de servicio de modelos con servicio de predicción, mantenimiento predictivo y recursos aprovisionados usando Azure Machine Learning y Azure Blob Storage.

---
## Cambios en la documentación
---
### Versión 1.0 (MLOPs)
- Implementación inicial de la pipeline de MLOps para predecir la probabilidad de enfermedades basándose en los síntomas de los pacientes.
- **Caso de Estudio**: Enfocado en predecir enfermedades usando el "Conjunto de Datos de Pacientes: Datos Demográficos y Clínicos" con 1500 registros, incluyendo datos demográficos (edad, género, etnia, estado civil, nivel educativo) y clínicos (fecha de diagnóstico, duración de síntomas, diagnósticos previos).
- **Entrada de Datos**: Utilizó Azure Blob Storage para registros médicos no estructurados y Azure Synapse Analytics para almacenamiento y consulta de datos estructurados.
- **Entrenamiento Offline**: Introdujo Análisis Exploratorio de Datos (EDA), Análisis de Componentes Principales (PCA), extracción de características y agregaciones usando bibliotecas de Python (pandas, NumPy, Jupyter, Learn), con entrenamiento y optimización de modelos mediante PyCaret y GitHub Actions.
- **Selección y Evaluación de Modelos**: Comparó modelos usando ROC AUC, F1-score, precisión y matriz de confusión, con validación cruzada k-fold y visualización mediante Matplotlib y MLflow.
- **Despliegue del Modelo**: Serializó modelos (pickle, protobuf) y los desplegó usando Azure HDInsight o Databricks con Spark para procesamiento de big data.
- **Predicciones del Modelo**: Proporcionó disponibilidad 24/7 para predicciones en tiempo real, almacenando resultados en Azure Storage.
- **Monitoreo**: Recomendó Azure Monitor para detectar problemas de calidad de datos y degradación del modelo, con posibles ciclos de reentrenamiento.

### Versión 2.0 (MLOPsv2)
- **Caso de Estudio**: Ampliado para enfatizar el desafío de la escasez de datos para enfermedades raras y la necesidad de modelos predictivos innovadores.
- **Entrada de Datos**: Mejorado con conectores API para integración de datos externos e introdujo Dipper para verificar deriva de datos.
- **Pipeline de Ingeniería de Características**: Agregó limpieza de datos, PCA, selección de características y un Feature Store usando Featuretools y Feast, junto con Azure Synapse Analytics y Databricks.
- **Iteraciones del Modelo**: Introdujo experimentos orquestados con pasos automatizados de Validación de Datos, Preparación, Entrenamiento, Evaluación y Validación usando tecnologías de Azure y PyCaret.
- **Selección y Evaluación de Modelos**: Mejoró la comparación con métricas detalladas y análisis de complejidad, guardó parámetros/artefactos del modelo e integró Azure Machine Learning para registro de modelos.
- **Despliegue del Modelo**: Pipeline CI/CD automatizada con frontend (Nginx) y backend (FastAPI) contenerizados, desplegados mediante Azure Kubernetes Service (AKS) como opción, y servicio de predicción continuo.
- **Predicciones del Modelo**: Mantuvo disponibilidad 24/7 con almacenamiento estructurado en Azure Storage, agregó estructura de proyecto con instrucciones de Docker Compose.
- **Monitoreo**: Enfatizó el Monitoreo Continuo (CM) con Azure Monitor para detección de deriva y disparadores de reentrenamiento automático.

### Versión 3.0 (MLOPsv3)
- **Caso de Estudio**: Mantuvo el enfoque en los desafíos de enfermedades raras, con mayor énfasis en metodologías innovadoras.
- **Entrada de Datos**: Mejorado con integración detallada de conectores API (REST/SOAP) para sistemas de terceros, reforzando disparadores de entrenamiento continuo.
- **Pipeline de Ingeniería de Características**: Mantuvo limpieza de datos, PCA y Feature Store, con uso mejorado de Azure Synapse Analytics y Databricks.
- **Iteraciones del Modelo**: Conservó experimentos orquestados, añadiendo Azure Machine Learning para comparación y validación robustas.
- **Selección y Evaluación de Modelos**: Mejorado con validación cruzada k-fold, soporte del SDK de Azure ML y paneles de rendimiento detallados, enfocándose en criterios comerciales y regulatorios.
- **Despliegue del Modelo**: Pipeline automatizada avanzada con Azure Data Factory para extracción de datos, Great Expectations para validación, y Azure ML Classic Web Service para despliegue escalable.
- **Predicciones del Modelo**: Actualizado a Azure Machine Learning Classic Web Service con API RESTful, añadió seguridad (TLS, AES-256, RBAC) y cumplimiento (HIPAA, GDPR), con almacenamiento estructurado en Azure Blob/Table/Cosmos DB.
- **Monitoreo**: Fortalecido con Azure Monitor, Microsoft Defender for Cloud y Azure Policy para monitoreo continuo, auditorías y disparadores de reentrenamiento, asegurando cumplimiento y escalabilidad.
- **Suscripción de Clientes**: Introdujo modelos de consumo flexibles (ejecución local o servicio en la nube) con autenticación (OAuth 2.0) y acceso basado en roles.


## Cambios en el repositorio

### 2025-05-18

### Añadidos y mejoras en GitHub Actions y Workflows

- **Feature/añadir GitHub actions** ([#17](https://github.com/cam2149/camartinez-mlops-U2/pull/17), [#11](https://github.com/cam2149/camartinez-mlops-U2/pull/11))
  - Se integraron y mejoraron flujos de trabajo con GitHub Actions para CI/CD.
  - Automatización de procesos de integración y despliegue.

- **jobs:** ([#16](https://github.com/cam2149/camartinez-mlops-U2/pull/16))
  - Añadido job `build-and-push` para automatizar la construcción y subida de imágenes Docker.
  - Configuración de permisos para paquetes.

- **Construcción y subida de imágenes Docker**
  - **Backend** ([#15](https://github.com/cam2149/camartinez-mlops-U2/pull/15)): Añadido workflow para construir y subir la imagen Docker de `Dockerfile.backend`.
  - **Frontend** ([#14](https://github.com/cam2149/camartinez-mlops-U2/pull/14)): Añadido workflow para construir y subir la imagen Docker de `Dockerfile.frontend`.

- **Etiquetado de imágenes** ([#13](https://github.com/cam2149/camartinez-mlops-U2/pull/13))
  - Se añadió el tag `ghcr.io/cam2149/camartinez-mlops-u2:latest` al flujo de trabajo de Docker.

- **Disparadores del workflow** ([#12](https://github.com/cam2149/camartinez-mlops-U2/pull/12))
  - Configuración del workflow para ejecutarse sobre la rama `main`.

### Pruebas y ajustes en workflows

- **Prueba pull requets** ([#10](https://github.com/cam2149/camartinez-mlops-U2/pull/10))
  - Pull request de prueba para validar flujos de trabajo.

- **Ajuste Actions** ([#9](https://github.com/cam2149/camartinez-mlops-U2/pull/9))
  - Ajustes menores en los workflows de Actions.

- **Prueba pullrequest actions** ([#8](https://github.com/cam2149/camartinez-mlops-U2/pull/8))
  - Pruebas adicionales para validar integraciones de Actions.

---

Para más detalles de cada cambio, consulta la sección de pull requests cerrados en el repositorio:  
https://github.com/cam2149/camartinez-mlops-U2/pulls?state=closed