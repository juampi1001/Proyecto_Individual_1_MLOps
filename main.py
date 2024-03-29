from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import traceback  
from typing import List, Dict
import pandas as pd
from Funciones import Developer,userdata,UserForGenre,best_developer_year,developer_reviews_analysis,recomendacion

app = FastAPI()

@app.get("/")
async def root():
    """
    "Proyecto Individual N° 1 - Juan Pablo Vitalevi"

    Versión: 1.0.0

    ---

    """
    return {"Mensaje": "Proyecto Individual N° 1 - Juan Pablo Vitalevi"}



@app.get("/recomendacion/{item_id}", tags=['recomendacion'])
async def item(item_id: str):
    '''
    Descripción: Ingresando el id de producto, devuelve una lista con 5 juegos recomendados similares al ingresado.
    
    Parámetros:
        - item_id (str): Id del producto para el cual se busca la recomendación. Debe ser un número, ejemplo: 761140
        
    Ejemplo de retorno: ["Surgeon Simulator","Urja",Pixel Puzzles 2: Anime",World of Cinema - Directors Cut",Train Valley"]
    '''

    resultado = recomendacion(item_id)
    return resultado
    

# endpoint 1 - developer
@app.get("/Developer/{desarrolladora}", tags=['Developer'])
async def endpoint1(desarrolladora: str):
    """
    Descripción: Retorna la cantidad de items y porcentaje de contenido Free por año 
    según empresa desarrolladora
    
    Parámetros:
        - desarrolladora (str): desarrolladora para la cual se 
          busca la cantidad de items y porcentaje free por anio. Debe ser un string, ejemplo: valve
    
    """
    try:
        # Validación adicional para asegurarse de que desarrolladora no sea nulo o esté vacío
        if not desarrolladora:
            raise HTTPException(status_code=422, detail="El parámetro 'desarrolladora' no puede ser nulo o estar vacío.")

        result = Developer(desarrolladora)

        # Validación para verificar si la desarrolladora existe en los datos
        if result.empty:
            raise HTTPException(status_code=404, detail=f"No se encontró información para la desarrolladora '{desarrolladora}'.")
            
        # Convierte el DataFrame a una lista de diccionarios
        data = result.reset_index().to_dict(orient="records")
        
        return data
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo developer.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# endpoint 2 - userdata
@app.get("/userdata/{user_id}", tags=['userdata'])
async def endpoint2(user_id: str):
    '''
    Descripción: Retorna cantidad de dinero gastado por el usuario, el porcentaje de 
    recomendación en base a reviews.recommend y cantidad de items

    Parámetros:
        - userid (str): usuario para el cual se busca el la cantidad de dinero gastado, porcentaje de recomendaciones y cantidad de items
        . Debe ser un string, ejemplo: doctr
    '''
    try:
        # Validación adicional para asegurarse de que el user_id no sea nulo o esté vacío
        if not user_id or not user_id.strip():
            raise HTTPException(status_code=422, detail="El parámetro 'user_id' no puede ser nulo o estar vacío.")

        result = userdata(user_id)
        
        # Validación para verificar si el user_id existe en los datos
        if not result:
            raise HTTPException(status_code=404, detail=f"No se encontró información para el usuario '{user_id}'.")
            
        return result
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo userdata.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# endpoint3 UserForGenre
@app.get("/UserForGenre/{genero}", tags=['UserForGenre'])
async def endpoint3(genero: str):
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
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo UserForGenre.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# endpoint4 best_developer_year
@app.get("/best_developer_year/{year}", tags=['best_developer_year'])
async def endpoint4(year: str):
    """
    Descripción: Segun el año, devuelve top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. 
    (reviews.recommend = True y comentarios positivos)
    Parámetros:
        - year (str): año para el cual se busca las 3 mejores desarrolladoras.ejemplo: 2015
    """
    try:
        result = best_developer_year(year)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo best_developer_year.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# endpoint5 developer_reviews_analysis
@app.get("/developer_reviews_analysis/{desarrolladora}", tags=['developer_reviews_analysis'])
async def endpoint5(desarrolladora: str):
    """
    Descripción: Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
    
    Parámetros:
        - desarrolladora (str): Nombre de la empresa desarrolladora para la cual se realiza el análisis de sentimiento. Debe ser un string, ejemplo: Valve
    
    Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}
    """
    try:
        result = developer_reviews_analysis(desarrolladora)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo developer_reviews_analysis.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


