# Proyecto_Steam_Games
API para consultas especificas de juegos


![Alt text](image.png)

Para la realizacion de este proyecto se sumnistró una base de datos correspondiente a juegos, esta informacion está entre los años 1983 hasta 2021 y se encuentra contenido en  archivos .json 
- 'australian_user_reviews.json'
- 'australian_users_items.json'
- 'output_steam_games.json'

Para el archivo -'output_steam_games.json' , en esta data tiene los campos 'publisher','genres', 'app_name', 'title', 'url', 'release_date', 'tags', 'discount_price', 'reviews_url', 'specs', 'price', 'early_access', 'id', 'developer', 'sentiment', 'metascore'.
Para el archivo - 'australian_users_items.json', en esta dat tiene los campos 'user_id', 'items_count', 'steam_id', 'user_url', 'items'.
Para el archivo - 'australian_user_reviews.json', en esta data tiene los campos 'user_id', 'user_url', 'reviews'.


Al obtener esta informacion se inicia con el estudio y trabajo de la data, es decir con el ETL  , donde según nuestra consideracion se realizan transformaciones necesarias que nos suminisre una data preparada de utilidad hacia el objetivo del proyecto.

Con esta informacion el paso a seguir es realizar  transformaciones de los datos para su procesamiento. En el archivo ETL.ipynb se encuentra el desarrollo de extraccion y transformacion de los datos, los cuales fueron:

1.  Importamos las librerias ast y pandas.

2.  Se abren los archivos en formato json 'output_steam_games.json','australian_users_items.json', 'australian_user_reviews.json'.

3.  Para cada dataset, se toma a considerar campos especificos y crear nuevos datasets, los cuales son requeridos para el  desarrollo de las funciones
3.1 En 'output_steam_games.json' se seleccionan las columnas 'id', 'genres','app_name','release_date'.
3.2 En 'australian_users_items.json' se seleccion las columnas 'item_id', 'playtime_forever', 'user_id'.
3.3 En 'australian_user_reviews.json' se seleccionan todas las columnas.

4. Transformaciones necesarias en cada dataset
4.1 'output_steam_games.json'
4.1.1 Se observa la informacion que contiene los datos, tipo de dato, cantidad, nulos.
4.1.2 Se muestran y eliminan los nulos.
4.1.3 En el campo 'id', se cambia a tipo de dato 'int'
4.1.4  Se crea una funcion para aplicar al campo 'release_date' cuya finalidad es identifacr los registros que no contienen el formato fecha yy-mm-dd pero que si tienen el año especifico, para despues convertir el registro  al formato yy-mm-dd.
4.1.5 Al campo 'release_date' se transforma a datatime.
4.1.6 Se extrae el año especifico a el campo 'release_date' y se crea la columna 'year'.
4.1.1 Se guarda y se crea el archivo 'steam.csv'.

4.2 'australian_users_items.json'
4.2.1 Se observa la informacion que contiene los datos, tipo de dato, cantidad, nulos.
4.2.2 En el campo 'item' se encuentran listas de diccionarios, se utiliza la funcion 'json_normsliza' para desanidar, y se obtienen campos 'item_name','items_count','steam_id', 'playtime_2weeks', 'playtime_forever'.
4.2.3 Se eliminan los campos que son itracendentes para la utilidad de este dataset en las consultas 'item_name','items_count','steam_id', 'playtime_2weeks'.
4.2.4 Se eliminan los duplicados.
4.2.5 Este dataset tiene un peso de mas 300 mb, para ser de utilidad en las consultas, es necesario cumplir con los requirimientos minimos de github para subir al repositorio, por ende se realiza un sample del 65%.
4.2.6 Se guarda y se extrae el archivo como 'df_items.csv'.

4.3 'australian_user_reviews.json'.
4.3.1 Se observa la informacion que contiene los datos, tipo de dato, cantidad, nulos.
4.3.2 El campo review esta anidado, por medio de un For, se puede acceder a los campos dentro del campo reviews y obtener los campos.
4.3.3 Se crea la funcion sentimient para  aplicar análisis de sentimiento con NLP 
debe tomar el valor '0' si es malo, '1' si es neutral y '2' si es positivo.
4.3.4 Se le aplica la funcion sentiment a 'review' y se crea en una nueva columna llamada 'sentiment_analisy', luego se elimina 'review'. 
4.3.5 Se guarda y se extrae el archivo como 'reviuws.csv'.

Al finalizar el prceso de ETL, se obtiene los archivos 'steam.csv', 'df_items' y 'revius.csv'.

Despues de haber hecho las transformaciones necesarias el paso a seguir es el desarrollo de las funciones. En el archivo FUNCIONES.ipynb, con los archivos extraidos en el ETL se toman consideraciones requeridas para desarrollar las funciones.

1. Se abren los archivos 'steam.csv', 'df_items' y 'revius.csv'.
2. Se observa la informacion y la composicion de cada dataset.
3. Se crean las funciones, para estas se realizan transformaciones con los dataset implicados.
3.1 Para la primera funcion PlayTimeGenre(genero): Debe devolver año con mas horas jugadas para dicho género y la segunda funcion UserForGenre(genero): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año, se hicieron las sgtes modificaciones:
3.1.2 Se crea un dataframe 'genero' con las campos 'id','genres','year'.
3.1.3 Se crea un dataframe 'play' con los campos, 'item_id','user_id','playtime_forever'.
3.1.4 Se realiza la union de los dataframe anteriores para crear 'generos'.
3.1.5 Al campo genres se le aplica ast.literal_eval para las listas de generos.
3.1.6 Se crea cada genero como un nuevo registro.
3.1.7 Se crea 'generos1' con los campos 'user_id','genres','year','playtime_forever'.
3.1.8 El dataset 'generos1' tiene un peso mayor al minimo requerido por github a subir al repositorio, este siendo un ejercicio netamente educativo se toma la desicion de trabajar solo con el 40% de los datos en aras de cumplir con el objetivo del proyecyo.
3.1.9 Se exporta y guarda el archivo como 'generos1.csv'.

3.2 Para las funciones UsersRecommend(año): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales) y UsersNotRecommend(año): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.(reviews.recommend = False y comentarios negativos) se hicieron las siguiente modificaciones:
3.2.1 Se Crea un dataframes año_game, compuesto con los campos 'id', 'app_name','year'.
3.2.2 Se renombra la columna 'id' a item_id.
3.2.3 Se eliminan los duplicados.
3.2.4 Se crea el dataframe recomendado, con los campos 'item_id','recommend','sentiment_analisy'.
3.2.5 Se une el Dataframe 'año_game' a 'recomendado'.
3.2.6 Se exporta y guarda el archivo como 'recomendado.csv'.

3.3 Para la funcion sentiment_analysis(año): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento. se hicieron las siguientes cambios:
3.3.1 Se crea el dataframe 'sentimiento', con los campos 'item_id','sentiment_analisy'.
3.3.2 Se une el Dataframe 'año_game' a 'sentimiento'.
3.3.3 Se exporta y guarda el archivo como 'sentiment.csv'.













Al finalizar esta transformaciones el siguiente paso es realizar son las funciones demandadas para la creacion de la API. Para el desarrollo de la API con el dataset final se obtiene los datos necesarios para la creacion de la API. para esto se hace necesario FastAPI que permite crear aplicaciones en menos tiempo y requiere menos esfuerzo. y Render crear una imagen o vídeo con el que mostrar un concepto, idea o proyecto de forma digital y realista.

a la API se le suministran las siguiente funciones:

 1. def genero( Año: str ): Se ingresa un año y devuelve una lista con los 5 géneros más ofrecidos en el orden correspondiente.

2. def juegos( Año: str ): Se ingresa un año y devuelve una lista con los juegos lanzados en el año.

3. def specs( Año: str ): Se ingresa un año y devuelve una lista con los 5 specs que más se repiten en el mismo en el orden correspondiente.

4. def earlyacces( Año: str ): Cantidad de juegos lanzados en un año con early access.

5. def sentiment( Año: str ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros que se encuentren categorizados con un análisis de sentimiento.

6. def metascore( Año: str ): Top 5 juegos según año con mayor metascore.

Y por último, crear un modelo de predicción en el que, con las variables elejidas (metascore, y género), deberíamos predecir el precio del juego y el RMSE del modelo

CONTENIDO DEL REPOSITORIO
- ENTORNO VIRTUAL
- data_games.csv
- Diccionario de Datos.xlsx
- ETL-Steam_Games.pynb
- image.png
- requirements.txt
- steam_games

LINKS DE LA API 

- https://steam-ratg.onrender.com



 
 



