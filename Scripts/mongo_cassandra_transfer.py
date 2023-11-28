from cassandra.cluster import Cluster
from pymongo import MongoClient

#el url se puede consultar en el docker, es el nombre del contenedor
cliente = MongoClient("mongodb://localhost:27017/")

#Nombre de la base de datos
db = cliente["Disney"]

#Nombre de la coleccion
coleccion = db["personajes"]

# Conexión a Cassandra
cluster = Cluster(['localhost:9042'])
cassandra_session = cluster.connect('tu_keyspace')#reemplazar por el keyspace en cassandra (tarea)

# Obtener datos de MongoDB
mongo_data = coleccion.find({})  # Ajustar la consulta

# Cerrar conexiones
cliente.close()
cluster.shutdown()