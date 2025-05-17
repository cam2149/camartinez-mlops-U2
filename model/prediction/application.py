from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
import pandas as pd
import random
import os


app = FastAPI(
    title="Predicción de Estado de Salud",
    description="API para predecir el estado de salud basado en edad, sexo e índice arterial.",
    version="1.0.0"
)

   # Configurar CORS
app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Permite todos los orígenes (ajusta según necesidad)
       allow_credentials=True,
       allow_methods=["GET"],
       allow_headers=["*"],
   )
       
@app.get("/getprediction",
    summary="Obtener predicción de estado de salud",
    description="Devuelve un estado de salud ('NO ENFERMO', 'ENFERMEDAD LEVE', 'ENFERMEDAD AGUDA', 'ENFERMEDAD CRÓNICA') basado en la edad, sexo e índice arterial.",
    response_description="Un objeto JSON con el estado de salud predicho.",
    )
def get_prediction(
    age: int,  
    sex: str, 
    arterialIndex: int
    ):
    
     # Validar parámetros de entrada
    if age < 0:
        raise HTTPException(status_code=400, detail="La edad debe ser un valor no negativo.")
    if arterialIndex < 0:
        raise HTTPException(status_code=400, detail="El índice arterial debe ser un valor no negativo.")
    
    # Leer el archivo CSV
    """
    Predice el estado de salud basado en parámetros de entrada.
    
    Args:
        ege (int): Edad del paciente.
        sex (str): Sexo del paciente (por ejemplo, 'M' o 'F').
        arterialIndex (int): Índice arterial del paciente.
    
    Returns:
        dict: Estado de salud predicho.
    """
    
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))
       
    try:
        df = pd.read_csv('/app/prediction/model.csv')
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo model.csv no encontrado.")
    
    # Filtrar datos según las reglas
    if arterialIndex <= 120:
        filtered_df = df[df['estado'] == 'NO ENFERMO']
    elif 20 <= age <= 39:
        if sex == 'M' and 162 <= arterialIndex <= 179:
            filtered_df = df[df['estado'] == 'ENFERMEDAD LEVE']
        elif sex == 'F' and 157 <= arterialIndex <= 176:
            filtered_df = df[df['estado'] == 'ENFERMEDAD LEVE']
        else:
            filtered_df = df[df['estado'] == 'INDETERMINADO']
    elif 40 <= age <= 59:
        if sex == 'M' and 180 <= arterialIndex <= 199:
            filtered_df = df[df['estado'] == 'ENFERMEDAD AGUDA']
        elif sex == 'F' and 180 <= arterialIndex <= 201:
            filtered_df = df[df['estado'] == 'ENFERMEDAD AGUDA']
        else:
            filtered_df = df[df['estado'] == 'ENFERMEDAD AGUDA']
    elif age >= 60:
        if sex == 'M' and 189 <= arterialIndex <= 213:
            filtered_df = df[df['estado'] == 'ENFERMEDAD CRÓNICA']
        elif sex == 'F' and 200 <= arterialIndex <= 225:
            filtered_df = df[df['estado'] == 'ENFERMEDAD CRÓNICA']
        else:
            filtered_df = df[df['estado'] == 'ENFERMEDAD AGUDA']
    else:
        filtered_df = df[df['estado'] == 'ENFERMEDAD AGUDA']

    
    
    # Si no hay registros que coincidan, devolver un estado por defecto
    if filtered_df.empty:
        return {"estado": "ENFERMEDAD AGUDA"}
    
    # Seleccionar aleatoriamente un estado de los registros filtrados
    estado = random.choice(filtered_df['estado'].tolist())
    
    return {"estado": estado}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)