from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import traceback  
from typing import List, Dict
import pandas as pd
from Funciones import Developer, UserForGenre

app = FastAPI()

@app.get("/")
async def root():
    """
    Proyecto FastAPI - Sistema de Recomendaciones

    Versión: 1.0.0

    ---

    """
    return {"Mensaje": "Proyecto Individual N° 1 - Juan Pablo Vitalevi"}

# endpoint 1 - developer

@app.get("/Developer/{desarrolladora}", tags=['Developer'])
async def endpoint1(desarrolladora: str):
    """
    Descripción: Retorna la cantidad de items y porcentaje de contenido Free por año 
    según empresa desarrolladora
    
    Parámetros:
        - desarrolladora (str): desarrolladora para la cual se 
        - busca la cantidad de items y porcentaje free por anio. Debe ser un string, ejemplo: valve
    
    """
    try:
        # Validación adicional para asegurarse de que desarrolladora no sea nulo o esté vacío
        if not desarrolladora:
            raise HTTPException(status_code=422, detail="El parámetro 'desarrolladora' no puede ser nulo o estar vacío.")

        result = Developer(desarrolladora)
        print("Resultado de Developer():", result)

            # Validación para verificar si la desarrolladora existe en los datos
        if not result:
            raise HTTPException(status_code=404, detail=f"No se encontró información para la desarrolladora '{desarrolladora}'.")
            
        # Convierte el DataFrame a una lista de diccionarios
        data = result.reset_index().to_dict(orient="records")
        
        return data
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo developer.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# endpoint2 UserForGenre
@app.get("/UserForGenre/{genero}", tags=['UserForGenre'])
async def endpoint2(genero: str):
    """
    Descripción: Retorna el usuario que acumula más horas jugadas para un género dado y una lista de la acumulación de horas jugadas por año.

    Parámetros:
        - genero (str): Género para el cual se busca el usuario con más horas jugadas. Debe ser un string, ejemplo: Adventure

    Ejemplo de retorno: {"Usuario con más horas jugadas para Género Adventure": Evilutional, Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
    """
    try:
        # Validación adicional para asegurarse de que el género no sea nulo o esté vacío
        if not genero or not genero.strip():
            raise HTTPException(status_code=422, detail="El parámetro 'genero' no puede ser nulo o estar vacío.")

        result = UserForGenre(genero)
        
        # Validación para verificar si el género existe en los datos
        if not result:
            raise HTTPException(status_code=404, detail=f"No se encontró información para el género '{genero}'.")
            
        return result
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo UserForGenre.csv: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

