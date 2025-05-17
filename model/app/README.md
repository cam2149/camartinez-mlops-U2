# Prediction Appplication

## Build the Docker image

Para crear la imagen, asegúrese de que la terminal esté dentro de la carpeta de la aplicación y ejecute.

```bash
docker build --pull --rm -f 'model\Dockerfile' -t 'mlopssample:latest' 'model' 
```

## Run the container

Para ejecutar el contenedor, asegúrese de crear primero la imagen y que la terminal esté dentro de la carpeta de la aplicación antes de ejecutarlo.

```bash
docker run -p 5000:5000 mlopssample:latest 
```
