from model import diagnosticos
from fastapi import FastAPI
import uvicorn
import logging
import os

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/')
async def root():  
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": "Bienvenido a la App de predicción de diagnóstico "+__name__+"."}


@app.post('/predictions')
async def procesar_diagnostico():
    """
    Endpoint para recibir datos y devolver una predicción.
    """
    logger.info("Recibiendo datos para predicción")
    try :
        prediction = diagnosticos()
        print("Predicción en Application.py:", prediction)  
    except Exception as e:
         
        print(f"Error en la predicción: {e}")    
        return {"error": "Error en la predicción"}
    return {'diagnostico': prediction[0]}

if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=5000, reload=True)
