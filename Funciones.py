#!/usr/bin/env python
# coding: utf-8

# ### Funciones para Endpoints / ML

# En esta sección, nos centraremos en consumir los archivos que se generaron en el notebook **datos_y_funciones**. que serán utilizadas por la API. El objetivo principal es dar respuestas a los Endpoints y a los Modelos Machine Learning, garantizando rapidez y eficacia en la ejecución de la API.

# In[6]:


import pandas as pd
import os


# ### Endpoint 1

# def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año 
# según empresa desarrolladora
# Input: **Developer.parquet**

def Developer(desarrolladora: str):
    df = pd.read_parquet('Datasets/archivos_API/Developer.parquet')
    
    # Filtrar el DataFrame por la desarrolladora específica
    df_desarrolladora = df[df['developer'] == desarrolladora.lower()]
    
    if df_desarrolladora.empty:
        raise ValueError(f"No hay datos disponibles para la desarrolladora '{desarrolladora}'.")
    
    # Eliminar filas con valores nulos en la columna 'release_year'
    df_desarrolladora = df_desarrolladora.dropna(subset=['release_year'])
    
    cantidad_items_por_anio = df_desarrolladora.groupby('release_year').size()
    
    df_free = df_desarrolladora[df_desarrolladora['price'] == 0]
    
    porcentaje_free_por_anio = (df_free.groupby('release_year').size() / cantidad_items_por_anio * 100).fillna(0).astype(int).astype(str) + "%"
    
    resultados = pd.DataFrame({
        'Cantidad de Items': cantidad_items_por_anio,
        'Contenido Free': porcentaje_free_por_anio
    })
    
    return resultados



    # ### Endpoint 2

# def UserForGenre( genre : str ): usuario que acumula más horas jugadas para un género dado 
# y una lista de la acumulación de horas jugadas por año.
 
# según empresa desarrolladora
# Input: **UserForGenre.parquet**
def UserForGenre(genero:str):
    consulta2 = pd.read_parquet('Datasets/archivos_API/UserForGenre.parquet')
    
    # Filtrar el DataFrame por el género dado
    genre_data = consulta2[consulta2['genres'] == genero.lower()]

    # Encontrar al usuario con más horas jugadas para ese género
    top_user = genre_data.loc[genre_data['hours_game'].idxmax()]['user_id']

    # Crear una lista de acumulación de horas jugadas por año
    hours_by_year = genre_data.groupby('release_year')['hours_game'].sum().reset_index()
  
    hours_by_year = hours_by_year.rename(columns={'release_year': 'Año', 'hours_game': 'Horas'})
    
    hours_list = hours_by_year.to_dict(orient='records')

    # Crear el diccionario de retorno
    result = {
        "Usuario con más horas jugadas para Género {}".format(genero): top_user,
        "Horas jugadas": hours_list
    }

    return result