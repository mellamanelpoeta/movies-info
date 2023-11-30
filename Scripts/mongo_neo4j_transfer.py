import pandas as pd
from neo4j import GraphDatabase
from pymongo import MongoClient
import json


mongo_uri = "mongodb://mongo:27017/"  # Cambia esto según tu configuración
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client["moviesdb"]
mongo_collection = mongo_db["movies"]

#Get data from mongo
cursor = mongo_collection.find()
df = pd.DataFrame(list(cursor))

'''LOCAL df = pd.read_json('movies.json')'''

#title,genre, release_date df
df.drop(columns=['_id','adult', 'backdrop_path', 'belongs_to_collection', 'budget', 'homepage','status', 
                        'tagline', 'video', 'vote_average', 'vote_count','imdb_id', 'original_language', 'original_title',
                        'overview', 'popularity', 'poster_path', 'revenue'], inplace=True)
df_normalized = df.explode('genres')
df_normalized['genres'] = df_normalized['genres'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
df_genero = df_normalized[['id','genres','title','release_date']]
df_genero['release_date'] = pd.to_datetime(df_genero['release_date'], format='%Y-%m-%d', errors='coerce')


uri = "bolt://neo4j:7687"  

# Load1
def load1(tx, movie_id, genre, title, release_date):
    year = release_date.year

    # Create nodes
    tx.run("""
        MERGE (g:Genre {name: $genre})
        MERGE (m:Movie {id: $id, title: $title})
        MERGE (y:Year {value: $year})
    """, genre=genre, id=movie_id, title=title, year=year)

    # Crea las relaciones ENTRE entre género, película y año
    tx.run("""
        MATCH (g:Genre {name: $genre})
        MATCH (m:Movie {id: $id})
        MATCH (y:Year {value: $year})
        MERGE (m)-[:IS_GENRE_OF]->(g)
        MERGE (m)-[:RELEASED_IN]->(y)
    """, genre=genre, id=movie_id, year=year)

# Load to neo4j
with GraphDatabase.driver(uri,auth=('neo4j', 'neoneo4j')) as driver:
    with driver.session() as session:
        for index, row in df_genero.iterrows():
            session.write_transaction(load1, row['id'], row['genres'], row['title'], row['release_date'])