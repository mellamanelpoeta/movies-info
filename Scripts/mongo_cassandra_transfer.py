from cassandra.cluster import Cluster
from pymongo import MongoClient

#Conexion a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["moviesdb"]
movies_collection = db["movies"]
credits_collection = db["credits"]

# Conexión a Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

#Seleccionas el keyspace
keyspace_name = "mov"
session.set_keyspace(keyspace_name)

#Elimar tablas existentes (si las hay)
session.execute("DROP TABLE IF EXISTS movie_cast")
session.execute("DROP TABLE IF EXISTS movies")

#Se crean las tablas
create_movie_cast_query = """
    CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id INT,
        cast_id INT,
        gender INT,
        name TEXT,
        character TEXT,
        popularity FLOAT,
        known_for_department TEXT,
        PRIMARY KEY (movie_id, cast_id)
    )
"""

create_movies_query = """
    CREATE TABLE IF NOT EXISTS movies (
        movie_id INT PRIMARY KEY,
        title TEXT,
        release_date DATE,
        genres SET<TEXT>,
        popularity FLOAT,
        budget FLOAT,
        revenue FLOAT,
        runtime INT,
        original_language TEXT,
        production_companies SET<TEXT>,
        production_countries SET<TEXT>,
        spoken_languages SET<TEXT>
    )
"""

session.execute(create_movie_cast_query)
session.execute(create_movies_query)

#Funcion para insertar datos en la tabla movie_cast
def insert_movie_cast(data):
    query = """
        INSERT INTO movie_cast (movie_id, cast_id, gender, name, character, popularity, known_for_department)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    prepared = session.prepare(query)
    for entry in data:
        movie_id = entry['id']  # El campo 'id' es el movie_id en Cassandra
        cast_list = entry['cast']

        for cast_member in cast_list:
            session.execute(prepared, (
                movie_id,
                cast_member['id'],  # El 'id' del elenco es el cast_id en Cassandra
                cast_member['gender'],
                cast_member['name'],
                cast_member['character'],
                cast_member['popularity'],
                cast_member['known_for_department']
            ))
    return

#Funcion para insertar datos en la tabla movies
def insert_movies(data):
    query = """
        INSERT INTO movies (movie_id, title, release_date, genres, popularity, budget, revenue, runtime, original_language, production_companies, production_countries, spoken_languages)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    prepared = session.prepare(query)
    for entry in data:
        try:
            # Establecer valores predeterminados si no existen datos en algunos campos
            production_companies = entry.get('production_companies', [])
            production_countries = entry.get('production_countries', [])
            spoken_languages = entry.get('spoken_languages', [])
            genres = entry.get('genres', [])

            session.execute(prepared, (
                entry['id'],
                entry['title'],
                entry['release_date'],
                set([genre['name'] for genre in genres]),
                entry['popularity'],
                entry['budget'],
                entry['revenue'],
                entry['runtime'],
                entry['original_language'],
                set([company['name'] for company in production_companies]),
                set([country['name'] for country in production_countries]),
                set([language['name'] for language in spoken_languages])
            ))
        except Exception as e:
            print(f"Error inserting entry: {entry}, Error: {str(e)}")
    return

#Insertar datos desde Mongo a Cassandra
cursor_movies = movies_collection.find({})
cursor_credits = credits_collection.find({})

insert_movies(cursor_movies)
insert_movie_cast(cursor_credits)


# Cerrar conexiones
client.close()
cluster.shutdown()
session.shutdown()