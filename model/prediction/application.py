from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
import pandas as pd
import json
import random
import os
from datetime import datetime
import pytz
from pydantic import BaseModel
from collections import Counter
from typing import List, Dict
import base64  # Standard library module, no external installation required

app = FastAPI(
    title="Predicción de Estado de Salud",
    description="API para predecir el estado de salud basado en edad, sexo e índice arterial, con reportes en Base64.",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Define response models
class PredictionResponse(BaseModel):
    estado: str
    timestamp: str

class ReportResponse(BaseModel):
    report_base64: str
    filename: str

# Define response model
class LastPredictionResponse(BaseModel):
    last_prediction_date: str
    estado: str
    
class HealthResponse(BaseModel):
    status: str
    
def load_conditions(json_path: str) -> dict:
    """Load health condition rules from a JSON file."""
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo conditions.json no encontrado.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Formato de JSON inválido en conditions.json.")

def save_prediction(estado: str, file_index: int):
    """Save prediction with timestamp to one of three JSON files."""
    timestamp = datetime.now(pytz.UTC).isoformat()
    prediction = {"estado": estado, "timestamp": timestamp}
    
    file_path = f'/app/prediction/predictions_{file_index}.json'
    try:
        # Load existing predictions
        try:
            with open(file_path, 'r') as f:
                predictions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            predictions = []
        
        # Append new prediction
        predictions.append(prediction)
        
        # Save updated predictions
        with open(file_path, 'w') as f:
            json.dump(predictions, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la predicción: {str(e)}")

@app.get("/getprediction",
    summary="Obtener predicción de estado de salud",
    description="Devuelve un estado de salud ('NO ENFERMO', 'ENFERMEDAD LEVE', 'ENFERMEDAD AGUDA', 'ENFERMEDAD CRÓNICA') basado en la edad, sexo e índice arterial.",
    response_description="Un objeto JSON con el estado de salud predicho y timestamp.",
    response_model=PredictionResponse
)
def get_prediction(age: int, sex: str, arterialIndex: int) -> PredictionResponse:
    """
    Predict health status based on input parameters and JSON conditions.
    
    Args:
        age (int): Patient's age
        sex (str): Patient's sex ('M' or 'F')
        arterialIndex (int): Patient's arterial index
    
    Returns:
        PredictionResponse: Predicted health status with timestamp
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

    # If no matching records, use the predicted status
    if filtered_df.empty:
        final_estado = estado
    else:
        # Randomly select a status from filtered records
        final_estado = random.choice(filtered_df['estado'].tolist())

    # Save to one of three JSON files (random selection for load balancing)
    save_prediction(final_estado, random.randint(1, 3))

    return PredictionResponse(estado=final_estado, timestamp=datetime.now(pytz.UTC).isoformat())

@app.get("/health",
    summary="Verificar el estado de la API",
    description="Devuelve el estado de salud de la API.",
    response_description="Un objeto JSON con el estado 'ok' si la API está funcionando.",
    response_model=HealthResponse
)
async def health_check() -> HealthResponse:
    """Return the health status of the API."""
    return HealthResponse(status="ok")

@app.get("/prediction_counts",
    summary="Obtener conteo de predicciones por categoría",
    description="Devuelve el número total de predicciones realizadas para cada categoría de estado de salud.",
    response_description="Un objeto JSON con el conteo de predicciones por categoría."
)
def get_prediction_counts() -> Dict[str, int]:
    """Return the total number of predictions made for each health status category."""
    all_predictions = []
    for i in range(1, 4):
        file_path = f'/app/prediction/predictions_{i}.json'
        try:
            with open(file_path, 'r') as f:
                predictions = json.load(f)
                all_predictions.extend(predictions)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    
    # Count predictions by status
    counts = Counter(pred['estado'] for pred in all_predictions)
    return dict(counts)

@app.get("/last_predictions",
    summary="Obtener las últimas 5 predicciones",
    description="Devuelve las últimas 5 predicciones realizadas, ordenadas por fecha descendente.",
    response_description="Una lista de objetos JSON con estado y timestamp.",
    response_model=List[PredictionResponse]
)
def get_last_predictions() -> List[PredictionResponse]:
    """Return the last 5 predictions made, sorted by timestamp in descending order."""
    all_predictions = []
    for i in range(1, 4):
        file_path = f'/app/prediction/predictions_{i}.json'
        try:
            with open(file_path, 'r') as f:
                predictions = json.load(f)
                all_predictions.extend(predictions)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    
    # Sort by timestamp and take last 5
    sorted_predictions = sorted(all_predictions, key=lambda x: x['timestamp'], reverse=True)[:5]
    return [PredictionResponse(estado=p['estado'], timestamp=p['timestamp']) for p in sorted_predictions]

@app.get("/last_prediction_date",
    summary="Obtener la fecha de la última predicción",
    description="Devuelve la fecha y hora de la última predicción realizada.",
    response_description="Un objeto JSON con la fecha y hora de la última predicción."
)
def get_last_prediction_date() -> Dict[str, str]:
    """Return the date and time of the last prediction made."""
    all_predictions = []
    for i in range(1, 4):
        file_path = f'/app/prediction/predictions_{i}.json'
        try:
            with open(file_path, 'r') as f:
                predictions = json.load(f)
                all_predictions.extend(predictions)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    
    if not all_predictions:
        raise HTTPException(status_code=404, detail="No se han realizado predicciones.")
    
    # Find the most recent prediction
    latest_prediction = max(all_predictions, key=lambda x: x['timestamp'])
    return {"last_prediction_date": latest_prediction['timestamp']}

@app.get("/getReport",
    summary="Obtener reporte de predicciones en Base64",
    description="Genera un archivo TXT con los resultados de última predicción, conteo de predicciones por categoría y las últimas 5 predicciones, codificado en Base64.",
    response_description="Un objeto JSON con el reporte en formato Base64.",
    response_model=ReportResponse
)
def get_report() -> ReportResponse:
    """
    Generate a Base64-encoded TXT report containing:
    - Last prediction date
    - Prediction counts by category
    - Last 5 predictions
    """
    try:
        # Fetch data from existing endpoints
        last_date = get_last_prediction_date()
        counts = get_prediction_counts()
        last_predictions = get_last_predictions()

        # Create report content
        report_lines = [
            "Reporte de Predicciones de Estado de Salud",
            "=" * 45,
            "",
            f"Fecha de la última predicción: {last_date['last_prediction_date']}",
            "",
            "Conteo de predicciones por categoría:",
            "-" * 45
        ]
        
        for estado, count in counts.items():
            report_lines.append(f"{estado}: {count}")
        
        report_lines.extend([
            "",
            "Últimas 5 predicciones:",
            "-" * 45
        ])
        
        for pred in last_predictions:
            report_lines.append(f"Estado: {pred.estado}, Timestamp: {pred.timestamp}")
        
        # Combine lines into a single string
        report_content = "\n".join(report_lines)
        
        # Encode to Base64
        report_bytes = report_content.encode('utf-8')
        base64_encoded = base64.b64encode(report_bytes).decode('utf-8')
        
        return ReportResponse(report_base64=base64_encoded, filename='ReportePredicciones.txt')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el reporte: {str(e)}")

@app.get("/last_prediction",
    summary="Obtener la última predicción",
    description="Devuelve la fecha, hora y estado de la última predicción realizada.",
    response_description="Un objeto JSON con la fecha, hora y estado de la última predicción.",
    response_model=LastPredictionResponse
)
def get_last_prediction() -> Dict[str, str]:
    """Return the date, time, and state of the last prediction made."""
    all_predictions = []
    for i in range(1, 4):
        file_path = f'/app/prediction/predictions_{i}.json'
        try:
            with open(file_path, 'r') as f:
                predictions = json.load(f)
                all_predictions.extend(predictions)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    
    if not all_predictions:
        raise HTTPException(status_code=404, detail="No se han realizado predicciones.")
    
    # Find the most recent prediction
    latest_prediction = max(all_predictions, key=lambda x: x['timestamp'])
    return {
        "last_prediction_date": latest_prediction['timestamp'],
        "estado": latest_prediction['estado']
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)