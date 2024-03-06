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
    
    result = pd.DataFrame({
        'Cantidad de Items': cantidad_items_por_anio,
        'Contenido Free': porcentaje_free_por_anio
    })
    
    return result

# ### Endpoint 2

# def userdata( user_id : str ): cantidad de dinero gastado por el usuario, el porcentaje de 
# recomendación en base a reviews.recommend y cantidad de items.
# Input: **usardata.parquet**
def userdata(user_id: str):
    
    df = pd.read_parquet('Datasets/archivos_API/userdata.parquet')

    # Filtrar el DataFrame para obtener solo las filas correspondientes al usuario dado
    user_data = df[df['user_id'] == user_id]

    # Verificar si el usuario existe
    if user_data.empty:
        return f"El usuario '{user_id}' no existe."

    # Calcular la cantidad de dinero gastado por el usuario
    dinero_gastado = user_data['price'].sum()

    # Calcular el porcentaje de recomendación positivas en base a la columna 'recommend'
    total_recomendaciones = user_data['recommend'].count()  # Contar todas las recomendaciones
    recomendaciones_positivas = user_data[user_data['recommend'] == True]['recommend'].count()  # Contar las recomendaciones positivas
    porcentaje_recomendacion = (recomendaciones_positivas / total_recomendaciones) * 100

    # Obtener la cantidad de ítems adquiridos por el usuario
    cantidad_items = user_data.shape[0]

    # Crear un DataFrame con los resultados
    result = {
        'Usuario': [user_id],
        'Dinero gastado': [dinero_gastado],
        'porcentaje de Recomendación': [porcentaje_recomendacion],
        'Cantidad de Items': [cantidad_items]
    }

    return result

    # ### Endpoint 3

# def UserForGenre( genre : str ): usuario que acumula más horas jugadas para un género dado 
# y una lista de la acumulación de horas jugadas por año.

# Input: **UserForGenre.parquet**
def UserForGenre(genero:str):
    df = pd.read_parquet('Datasets/archivos_API/UserForGenre.parquet')
    
    # Filtrar el DataFrame por el género dado
    genre_data = df[df['genres'] == genero.lower()]

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