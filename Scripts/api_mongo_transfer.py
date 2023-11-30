import requests
from pymongo import MongoClient

#Configuracion de la clave de API de TMDb
bearer_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNDRhZDQ3NTAyNTNiMGIxM2FmMjJjNjIwNmE2MmNmMyIsInN1YiI6IjY1NjZhY2M1ZDk1NDIwMDExYjk1MmE1NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.N2gnv8B7AlaOmB_o4FXvv3T2saPCZU5dDFhs8i8IJJg"
base_url = "https://api.themoviedb.org/3"

#Configuracion de la conexion a MongoDB
#el url se puede consultar en el docker, es el nombre del contenedor
#cliente = MongoClient("mongodb://localhost:27017/")

#Nombre de la base de datos
#db = cliente["Movies"]


#Funcion para insertar informacion (en documentos json) a MongoDB
def insert_Mongo(coleccion, data):
    coleccion.insert_many(data)
    return

#Funcion para obtener informacion de peliculas de un año en particular
def moviesId_per_year(year):
    url = f"{base_url}/discover/movie"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    list_id = []

    #It gets the information of the top 100 movies of the year
    for i in range(1,6):
        
        params ={
        "primary_release_year": f"{year}",
        "page": f"{i}",
        "sort_by": "popularity.desc"
        }
        response = requests.get(url,headers=headers, params=params)
        results = response.json()["results"]
        if i == 1:
            print(response.json()["total_results"])
        
        for elem in results:
            list_id.append(elem['id'])
            print(elem['title'])
        
    return list_id

def movie_details(list_id):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }
   
    for id in list_id:
        url = f"{base_url}/movie/{id}?language=en-US"
        response = requests.get(url, headers=headers)
        results = response.json()["results"]
        
    return

def genres():
    url = f"{base_url}/genre/movie/list?language=en"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    response = requests.get(url,headers=headers)
    return response.json()["results"]


for year in range(1990,2024):
    print(year)
    moviesId_per_year(year)

#print(list_id)

#cliente.close()