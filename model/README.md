# Guía de Configuración y Ejecución del Proyecto

Este proyecto consta de una aplicación frontend y backend, contenerizadas usando Docker y orquestadas con Docker Compose. El frontend es un archivo HTML estático (`index.html`) servido por Nginx en el puerto 8000, y el backend es una aplicación FastAPI (`application.py`) ejecutándose en el puerto 5000. Este README proporciona instrucciones detalladas para construir y ejecutar cada componente individualmente usando `Dockerfile.frontend` y `Dockerfile.backend`, así como juntos usando `docker-compose.yml`.

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

Verifica las instalaciones:
```bash
docker --version
docker-compose --version
```

## Suposiciones

- El backend (`application.py`) es una aplicación FastAPI con una variable `app` definida (por ejemplo, `app = FastAPI()`).
- Existe un archivo `requirements.txt` en `model/prediction/` con dependencias como `fastapi==0.115.0` y `uvicorn==0.30.6`.
- El frontend (`index.html`) es un archivo estático servido por Nginx.
- El sistema tiene acceso a los puertos 8000 (frontend) y 5000 (backend). Si estos puertos están en uso, ajusta los mapeos de puertos en `docker-compose.yml` o detén los servicios en conflicto.

## Instrucciones Paso a Paso

### 1. Ejecutar el Frontend con `Dockerfile.frontend`

El `Dockerfile.frontend` construye una imagen basada en Nginx para servir el archivo estático `index.html` desde `model/frontend/` en el puerto 8000.

#### Pasos

1. **Navegar al Directorio del Proyecto**:
   Asegúrate de estar en el directorio raíz del proyecto donde se encuentra `Dockerfile.frontend`:
   ```bash
   cd ruta/a/your_project
   ```

2. **Verificar la Estructura del Proyecto**:
   Confirma que los archivos `model/frontend/index.html` y `nginx.conf` existen:
   ```bash
   ls -R
   ```
   La salida esperada incluye:
   ```
   Dockerfile.frontend  Dockerfile.backend  docker-compose.yml  nginx.conf  model
   ./model:
   frontend  prediction
   ./model/frontend:
   index.html
   ./model/prediction:
   application.py
   ```

3. **Construir la Imagen del Frontend**:
   Construye la imagen Docker usando `Dockerfile.frontend`:
   ```bash
   docker build -f Dockerfile.frontend -t frontend-image .
   ```
   - `-f Dockerfile.frontend`: Especifica el Dockerfile a usar.
   - `-t frontend-image`: Nombra la imagen como `frontend-image`.
   - `.`: Usa el directorio actual como contexto de construcción.

4. **Ejecutar el Contenedor del Frontend**:
   Ejecuta el contenedor, mapeando el puerto 8000 del host al puerto 8000 del contenedor:
   ```bash
   docker run -d -p 8000:8000 --name frontend-container frontend-image
   ```
   - `-d`: Ejecuta el contenedor en modo detached (en segundo plano).
   - `-p 8000:8000`: Mapea el puerto 8000 del host al puerto 8000 del contenedor.
   - `--name frontend-container`: Nombra el contenedor para referencia fácil.

5. **Verificar el Frontend**:
   Abre un navegador y navega a:
   ```
   http://localhost:8000
   ```
   Deberías ver el contenido de `index.html`. Alternativamente, usa `curl`:
   ```bash
   curl http://localhost:8000
   ```

6. **Detener y Limpiar**:
   Detén y elimina el contenedor cuando termines:
   ```bash
   docker stop frontend-container
   docker rm frontend-container
   ```

#### Solución de Problemas
- **"Puerto ya en uso"**:
  Verifica si el puerto 8000 está ocupado:
  ```bash
  lsof -i :8000
  ```
  Detén el proceso en conflicto o cambia el mapeo de puertos (por ejemplo, `-p 8080:8000`).
- **Error 404**:
  Asegúrate de que `model/frontend/index.html` exista y sea legible:
  ```bash
  cat model/frontend/index.html
  chmod -R u+r model
  ```
- **Fallo en la Construcción**:
  Verifica que `nginx.conf` y `model/frontend/` estén en el directorio raíz. Revisa los logs de construcción:
  ```bash
  docker build -f Dockerfile.frontend -t frontend-image .
  ```

### 2. Ejecutar el Backend con `Dockerfile.backend`

El `Dockerfile.backend` construye una imagen basada en Python para ejecutar la aplicación FastAPI (`application.py`) desde `model/prediction/` en el puerto 5000 usando Uvicorn.

#### Pasos

1. **Navegar al Directorio del Proyecto**:
   Asegúrate de estar en el directorio raíz:
   ```bash
   cd ruta/a/your_project
   ```

2. **Verificar Requisitos**:
   Confirma que `model/prediction/requirements.txt` exista e incluya:
   ```text
   fastapi==0.115.0
   uvicorn==0.30.6
   ```
   Revisa con:
   ```bash
   cat model/prediction/requirements.txt
   ```
   Si falta, créalo en `model/prediction/` con el contenido anterior.

3. **Verificar application.py**:
   Asegúrate de que `application.py` defina una aplicación FastAPI llamada `app`. Ejemplo:
   ```python
   from fastapi import FastAPI
   app = FastAPI()
   @app.get("/")
   async def root():
       return {"message": "¡Hola desde el backend FastAPI!"}
   ```
   Revisa:
   ```bash
   cat model/prediction/application.py
   ```

4. **Construir la Imagen del Backend**:
   Construye la imagen Docker usando `Dockerfile.backend`:
   ```bash
   docker build -f Dockerfile.backend -t backend-image .
   ```
   - `-f Dockerfile.backend`: Especifica el Dockerfile.
   - `-t backend-image`: Nombra la imagen como `backend-image`.

5. **Ejecutar el Contenedor del Backend**:
   Ejecuta el contenedor, mapeando el puerto 5000:
   ```bash
   docker run -d -p 5000:5000 --name backend-container backend-image
   ```

6. **Verificar el Backend**:
   Abre un navegador y navega a:
   ```
   http://localhost:5000/docs
   ```
   Esto carga la interfaz Swagger de FastAPI. Alternativamente, prueba el endpoint raíz:
   ```bash
   curl http://localhost:5000
   ```
   Respuesta esperada (basada en el ejemplo `application.py`):
   ```json
   {"message": "¡Hola desde el backend FastAPI!"}
   ```

7. **Detener y Limpiar**:
   Detén y elimina el contenedor:
   ```bash
   docker stop backend-container
   docker rm backend-container
   ```

#### Solución de Problemas
- **"uvicorn: comando no encontrado"**:
  Asegúrate de que `requirements.txt` incluya `uvicorn`. Verifica la instalación:
  ```bash
  docker run -it backend-image bash
  pip show uvicorn
  ```
  Si falta, actualiza `requirements.txt` y reconstruye.
- **Módulo No Encontrado**:
  Si `application.py` tiene dependencias adicionales, agrégalas a `requirements.txt`.
- **Aplicación FastAPI No Encontrada**:
  Si `application.py` usa un nombre de app diferente (por ejemplo, `api`), actualiza `Dockerfile.backend`:
  ```dockerfile
  CMD ["uvicorn", "prediction.application:api", "--host", "0.0.0.0", "--port", "5000"]
  ```
- **Conflicto de Puerto**:
  Revisa el puerto 5000:
  ```bash
  lsof -i :5000
  ```
  Usa un puerto diferente si es necesario (por ejemplo, `-p 5001:5000`).

### 3. Ejecutar Ambos Servicios con `docker-compose.yml`

El `docker-compose.yml` orquesta los servicios frontend y backend, construyéndolos desde `Dockerfile.frontend` y `Dockerfile.backend`, respectivamente, y conectándolos a través de una red bridge.

#### Pasos

1. **Navegar al Directorio del Proyecto**:
   ```bash
   cd ruta/a/your_project
   ```

2. **Verificar docker-compose.yml**:
   Asegúrate de que `docker-compose.yml` coincida:
   ```yaml
   version: '3.8'

   services:
     frontend:
       build:
         context: .
         dockerfile: Dockerfile.frontend
       ports:
         - "8000:8000"
       depends_on:
         - backend
       networks:
         - app-network

     backend:
       build:
         context: .
         dockerfile: Dockerfile.backend
       ports:
         - "5000:5000"
       networks:
         - app-network

   networks:
     app-network:
       driver: bridge
   ```

3. **Construir y Ejecutar**:
   Construye y ejecuta ambos servicios:
   ```bash
   docker-compose up --build
   ```
   - `--build`: Fuerza la reconstrucción de las imágenes para aplicar cambios.
   - Esto inicia ambos contenedores en primer plano, mostrando los logs.

   Para ejecutar en modo detached:
   ```bash
   docker-compose up -d --build
   ```

4. **Verificar Servicios**:
   - **Frontend**: Abre `http://localhost:8000` para ver `index.html`.
   - **Backend**: Abre `http://localhost:5000/docs` para la interfaz Swagger de FastAPI, o prueba:
     ```bash
     curl http://localhost:5000
     ```

5. **Ver Logs**:
   Revisa los logs para depuración:
   ```bash
   docker-compose logs
   ```
   O para un servicio específico:
   ```bash
   docker-compose logs backend
   ```

6. **Detener y Limpiar**:
   Detén y elimina contenedores, redes y volúmenes:
   ```bash
   docker-compose down
   ```
   Para eliminar también las imágenes:
   ```bash
   docker-compose down --rmi all
   ```

#### Solución de Problemas
- **Fallo en la Construcción**:
  Asegúrate de que todos los archivos (`model/frontend/index.html`, `model/prediction/application.py`, `nginx.conf`, `requirements.txt`) existan y sean legibles:
  ```bash
  chmod -R u+r model
  ```
- **Comunicación entre Servicios**:
  Si el frontend necesita llamar al backend, usa el nombre del servicio `backend` (por ejemplo, `http://backend:5000` desde el contenedor del frontend) debido a la red `app-network`.
- **Conflictos de Puerto**:
  Modifica los puertos en `docker-compose.yml` si es necesario (por ejemplo, `"8080:8000"` para el frontend).
- **Errores de Dependencias**:
  Revisa `requirements.txt` por paquetes faltantes. Reconstruye si se actualiza:
  ```bash
  docker-compose build backend
  ```

## Notas Adicionales

- **Personalizar Puertos**:
  Para cambiar puertos, edita `docker-compose.yml` (por ejemplo, `"8080:8000"` para el frontend) y asegúrate de que `nginx.conf` (para el frontend) o `Dockerfile.backend` (para el backend) refleje el puerto del contenedor.
- **requirements.txt**:
  Si `requirements.txt` está en el directorio raíz, actualiza `Dockerfile.backend`:
  ```dockerfile
  COPY requirements.txt /app/
  RUN pip install --no-cache-dir -r requirements.txt
  ```
- **Escalado**:
  Para escalar el backend (por ejemplo, ejecutar múltiples instancias):
  ```bash
  docker-compose up --scale backend=3
  ```
  Nota: Asegúrate de que el frontend esté configurado para manejar múltiples instancias del backend (por ejemplo, mediante un balanceador de carga).
- **Depuración**:
  Accede a la shell de un contenedor para depuración:
  ```bash
  docker-compose run backend bash
  ```

## Archivos de Ejemplo

Para referencia, asegúrate de las siguientes configuraciones:

- **application.py** (ejemplo):
  ```python
  from fastapi import FastAPI
  app = FastAPI()
  @app.get("/")
  async def root():
      return {"message": "¡Hola desde el backend FastAPI!"}
  ```

- **index.html** (ejemplo):
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <title>Frontend</title>
  </head>
  <body>
      <h1>Bienvenido al Frontend</h1>
  </body>
  </html>
  ```

## Soporte

Si encuentras problemas:
- Comparte la salida de `docker-compose logs` o errores específicos de construcción/ejecución.
- Proporciona el contenido de `requirements.txt` o `application.py` si los errores están relacionados con dependencias o configuración de la app.
- Confirma la estructura exacta del proyecto con:
  ```bash
  ls -R
  ```

¡Esta guía debería permitirte ejecutar con éxito el frontend, el backend y los servicios combinados! ¡Feliz codificación!