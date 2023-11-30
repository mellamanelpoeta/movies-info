#gguerr21@itam.mx
import pandas as pd
from py2neo import Graph, Node, Relationship
from pymongo import MongoClient

# Configuración de MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["nombre_de_tu_base_de_datos"]
mongo_collection = mongo_db["nombre_de_tu_coleccion"]

# Configuración de Neo4j
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "neo4j"

# Configuración de conexión a Neo4j
graph = Graph(neo4j_uri, auth=(neo4j_user, neo4j_password))

import pandas as pd
from pymongo import MongoClient

# Configuración de MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["nombre_de_tu_base_de_datos"]
mongo_collection = mongo_db["nombre_de_tu_coleccion"]

def obtener_datos_desde_mongo_a_dataframe():
    cursor = mongo_collection.find()

    # Crea un DataFrame a partir de los documentos
    dataframe = pd.DataFrame(list(cursor))

    return dataframe

if __name__ == "__main__":
    # Obtiene los datos desde MongoDB a un DataFrame de pandas
    df = obtener_datos_desde_mongo_a_dataframe()

    # Puedes realizar más procesamiento o análisis con el DataFrame aquí
    # ...

    # Muestra el DataFrame
    print(df)


def cargar_datos_desde_dataframe_a_neo4j(dataframe):
    for index, row in dataframe.iterrows():
        # Crea nodos y relaciones en Neo4j según tu lógica
        # Ejemplo:
        pelicula = Node("Pelicula", titulo=row["titulo"])
        actor = Node("Actor", nombre=row["actor"])
        relacion = Relationship(actor, "ACTUO_EN", pelicula)
        graph.create(relacion)

if __name__ == "__main__":
    # Lee tus datos desde MongoDB a un DataFrame de pandas
    # Puedes usar pd.read_json o pd.read_csv según el formato de tus datos
    dataframe = pd.read_json("datos.json")

    # Carga los datos en Neo4j
    cargar_datos_desde_dataframe_a_neo4j(dataframe)