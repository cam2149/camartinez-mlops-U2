from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
import pandas as pd
import json
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

def load_conditions(json_path: str) -> dict:
    """Load health condition rules from a JSON file."""
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo conditions.json no encontrado.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Formato de JSON inválido en conditions.json.")
           
@app.get("/getprediction",
    summary="Obtener predicción de estado de salud",
    description="Devuelve un estado de salud ('NO ENFERMO', 'ENFERMEDAD LEVE', 'ENFERMEDAD AGUDA', 'ENFERMEDAD CRÓNICA') basado en la edad, sexo e índice arterial.",
    response_description="Un objeto JSON con el estado de salud predicho.",
    )
def get_prediction(age: int, sex: str, arterialIndex: int) -> dict:
    """
    Predict health status based on input parameters and JSON conditions.
    
    Args:
        age (int): Patient's age
        sex (str): Patient's sex ('M' or 'F')
        arterialIndex (int): Patient's arterial index
    
    Returns:
        dict: Predicted health status
    """
    # Input validation
    if age < 0:
        raise HTTPException(status_code=400, detail="La edad debe ser un valor no negativo.")
    if arterialIndex < 0:
        raise HTTPException(status_code=400, detail="El índice arterial debe ser un valor no negativo.")
    if sex not in ['M', 'F']:
        raise HTTPException(status_code=400, detail="El sexo debe ser 'M' o 'F'.")

    # Load CSV data
    try:
        df = pd.read_csv('/app/prediction/model.csv')
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo model.csv no encontrado.")

    # Load conditions from JSON
    conditions = load_conditions('/app/prediction/conditions.json')

    # Evaluate conditions
    estado = None
    for condition in conditions['conditions']:
        age_range = condition['age_range']
        if age_range[0] <= age <= age_range[1]:
            for rule in condition['rules']:
                if rule['sex'] == sex and rule['arterial_index'][0] <= arterialIndex <= rule['arterial_index'][1]:
                    estado = rule['estado']
                    break
            if estado:
                break

    # Default case if no specific condition matches
    if not estado:
        if arterialIndex <= conditions['default_threshold']['arterial_index']:
            estado = 'NO ENFERMO'
        else:
            estado = 'ENFERMEDAD AGUDA'

    # Filter dataframe based on predicted status
    filtered_df = df[df['estado'] == estado]

    # If no matching records, return the predicted status
    if filtered_df.empty:
        return {"estado": estado}

    # Randomly select a status from filtered records
    estado = random.choice(filtered_df['estado'].tolist())
    return {"estado": estado}


    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)