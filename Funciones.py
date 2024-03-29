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

# ### Endpoint 4

# def best_developer_year( year : str ): top 3 de desarrolladores con 
# juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)

# Input: **best_developer_year.parquet**
def best_developer_year(anio):
    df = pd.read_parquet('Datasets/archivos_API/best_developer_year.parquet')

    # Filtrar el DataFrame por el año dado
    df_year = df[df['year'] == int(anio)] 
    
    # Contar la frecuencia de aparición de las desarrolladoras
    desarrolladora = df_year['developer'].value_counts()  
    
    # Obtener las tres dessarolladoras mas comunes
    podio = desarrolladora.head(3).reset_index().to_dict('records')
    
    return podio

# ### Endpoint 5

#def developer_reviews_analysis( desarrolladora : str ): Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como 
# llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis 
# de sentimiento como valor positivo, neutro o negativo.
def developer_reviews_analysis(desarrolladora: str):
    df = pd.read_parquet('Datasets/archivos_API/developer_reviews_analysis.parquet')

    # Filtrar por la empresa desarrolladora
    developer = df[df['developer'] == desarrolladora.lower()]

    # Convertir a formato de diccionario
    response_data = developer.set_index('developer').to_dict(orient='index')
    
    return response_data

# sistema de recomendacion item-item
def recomendacion(item_id: str):
    df = pd.read_parquet('Datasets/archivos_ML/recomienda_item_item.parquet')
    #castear el item_id para que coincida con el dtype del datafame
    item_id = int(item_id)
    
    # Verificar la existencia del item_id en el DataFrame
    if item_id not in df['item_id'].values:
        return f"No se encontraron recomendaciones para el item_id '{item_id}'."
    
    # Filtrar el DataFrame por el item_id especificado
    result_df = df[df['item_id'] == item_id]

    recomendaciones = list(result_df['RecomendacionesTop5'].iloc[0])

    
    return recomendaciones