from fastapi import FastAPI
import pandas as pd
import numpy as np




data = pd.read_csv('data_games.csv')

app = FastAPI()

@app.get('/genero/')

def genero(año:int):

  filtro = data[data['year'] == año]
  explode = filtro.explode('genres')
  top = explode['genres'].value_counts().nlargest(5).index.tolist()

  return {f'los 5 generos mas creados este año {año} son':top}

print(genero(2008))

@app.get('/juegos/')

def juegos(año:int):

    filtro = data[data['year'] == año] 
    game = filtro['title'].head(10).tolist()

    return {f'10 juegos lanzados este año {año} son':game}

@app.get('/specs/')

def specs(año:int):
    
    filtro = data[data['year'] == año]
    explode = filtro.explode('specs')
    top = explode['specs'].value_counts().nlargest(5).index.tolist()

    return {f'Las especificaciones mas repetidas este año {año} son':top}

@app.get('/earlyacces/')

def earlyacces(año:int):
    filtro = data[data['year'] == año]
    conteo_early = len(filtro[filtro['early_access'] == True])
    return {f'cantidad de juegos con acceso temprano este año {año} es':conteo_early} 

@app.get('/sentiment/')

def sentiment(año:int):

    filtro = data[data['year'] == año]
    conte_sentimen = filtro['sentiment'].value_counts().to_dict()
    return conte_sentimen

@app.get('/metascore/')

def metascore(año:int):
    filtro = data[data['year'] == año]
    top_juegos = filtro.sort_values(by='metascore', ascending = False)['title'][:5]

    return top_juegos.to_dict()