import requests
from pymongo import MongoClient

#El url de la api
url="https://api.disneyapi.dev/character/"

#el url se puede consultar en el docker, es el nombre del contenedor
cliente = MongoClient("mongodb://localhost:27017/")

#Nombre de la base de datos
db = cliente["Disney"]

#Nombre de la coleccion
coleccion = db["personajes"]

#Ciclo para insertar los personajes de Disney de la API
for numero_personaje in range(1, 7438):
    respuesta = requests.get(f"{url}{numero_personaje}")
    if respuesta.status_code == 200:
        datos_personaje = respuesta.json()
        
        #Se verifica que tenga datos, pues hay varios documentos
        #json en la API que vienen vacios, ej. 
        #{"info":{"count":0,"totalPages":0,"previousPage":null,"nextPage":null},"data":[]}
        if(len(datos_personaje['data'])!=0):
            name= datos_personaje['data']['name']
            coleccion.insert_one(datos_personaje)
            print(f"Guardado personaje #{numero_personaje}: ",name)
    else:
        print(f"No se pudo obtener el Pokémon #{numero_personaje}")

cliente.close()