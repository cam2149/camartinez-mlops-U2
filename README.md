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


