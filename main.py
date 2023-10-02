from fastapi import FastAPI
import pandas as pd
import numpy as np
from fastapi import HTTPException


generos1 = pd.read_csv('generos1.csv')
recomendado = pd.read_csv('recomendado.csv')
sentimento = pd.read_csv('sentiment.csv')



app = FastAPI()


@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):
    try:
        genero_df = generos1[generos1['genres'] == genero]
        
        
        if genero_df.empty:
            return {"error": f"El género {genero} no fue encontrado en los datos."}

        anio_con_max_horas = genero_df.groupby('year')['playtime_forever'].sum().idxmax()

        return {f'Año con mas horas jugadas del genero {genero}': int(anio_con_max_horas)}  # Convertimos a int
    except Exception as e:
        return {"error": str(e)}  # Manejamos cualquier excepción y la devolvemos como respuesta


@app.get('/UserForGenre/{genero}')

def UserForGenre(genero:str):
    
    
    genero_df = generos1[generos1['genres'].str.contains(genero, case=False)]
    
    usuario_mas_horas = genero_df.groupby('user_id')['playtime_forever'].sum().idxmax()
    
    usuario_genero_df = genero_df[genero_df['user_id'] == usuario_mas_horas]
    
    acumulacion_horas_por_anio = usuario_genero_df.groupby('year')['playtime_forever'].sum().reset_index()

    lista_acumulacion_horas = [{'año': año, 'horas': horas} for año, horas in zip(acumulacion_horas_por_anio['year'], acumulacion_horas_por_anio['playtime_forever'])]

    
    return {f'Usuario con mas horas jugadas para el genero {genero}': usuario_mas_horas, 'Horas jugadas': lista_acumulacion_horas}



@app.get('/UsersRecommend/{anio}')


def UsersRecommend(anio:int):

    try:
    
        filtered_df = recomendado[(recomendado['year'] == anio) & (recomendado['recommend'] == True) & (recomendado['sentiment_analisy'] >= 1)]
    
        game_counts = filtered_df['app_name'].value_counts().reset_index()
        game_counts.columns = ['app_name', 'count']

        sorted_games = game_counts.sort_values(by='count', ascending=False)
    
        top_3_games = sorted_games.head(3)

        if top_3_games.empty:
            raise HTTPException(status_code=404, detail="No se encontraron juegos recomendados para el año especificado.")

    # Crear la lista de diccionarios en el formato deseado
        result = [{"Puesto {}: {}".format(i+1, game['app_name'])} for i, game in top_3_games.iterrows()]
    
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/UsersNotRecommend/{año}')

def UsersNotRecommend(anio:int):

    try:

        filtered_df = recomendado[(recomendado['year'] == anio) & (recomendado['recommend'] == False) & (recomendado['sentiment_analisy'] == 0)]
    
        game_counts = filtered_df['app_name'].value_counts().reset_index()
        game_counts.columns = ['app_name', 'count']
    
        sorted_games = game_counts.sort_values(by='count', ascending=False)
    
        top_3_least_recommended = sorted_games.head(3)

        if top_3_least_recommended.empty:
            raise HTTPException(status_code=404, detail="No se encontraron juegos recomendados para el año especificado.")

        result = [{"Puesto {}: {}".format(i+1, game['app_name'])} for i, game in top_3_least_recommended.iterrows()]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        


@app.get('/sentiment_analysis/{anio}')

def sentiment_analysis(anio:int):
    

    año_reviu = sentimento[sentimento['year'] == anio]
    
    conteo_sentiment = {'Negative': 0, 'Neutral': 0, 'Positive': 0}
    
    for index, row in año_reviu.iterrows():
        sentiment = row['sentiment_analisy']
        categoria = ''
        
        if sentiment == 0:
            categoria = 'Negative'
        elif sentiment == 1:
            categoria = 'Neutral'
        elif sentiment == 2:
            categoria = 'Positive'
        
        # Incrementar el contador correspondiente en el diccionario
        conteo_sentiment[categoria] += 1
    
    return conteo_sentiment
