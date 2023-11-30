# ProyectoFinal_NoSQL
Proyecto en el que se demuestra el entendimiento y capacidad de manejo de las diferentes bases de datos que vimos en el semestre, así como los conceptos relacionados con API’s, ETL’s, etc.
El objetivo del proyecto es integrar los siguientes elementos:
- Realizar solicitudes a una API de nuestra elección;
- insertar las respuestas a las solicitudes a una base de datos en MongoDB, la cual funcionará como DataLake;
- del DataLake se deberá poder hacer consultas y un proceso de extracción, transformación y carga a otras dos bases de datos: Cassandra y Neo4j;
- incorporar todos los elementos dentro de un Docker-Compose.

A lo largo de este documento se explicará la API que se escogió, cómo funciona el proyecto, los requisitos para su ejecución en cualquier entorno local y algunas consultas para cada una de las bases de datos, junto con la explicación de los resultados que arrojan. 

## Acerca de la API: TMDB - The Movie Database API
[The Movie Database (TMDB)](https://www.themoviedb.org/) es una base de datos en línea que contiene una amplia gama de información sobre películas y programas de televisión. Ofrece detalles como el elenco, equipo de producción, fechas de estreno, sinopsis, clasificaciones, puntuaciones de usuarios y críticos, imágenes, tráilers, posters y entre otros. En la plataforma, los usuarios pueden contribuir agregando información, corrigiendo errores o añadiendo contenido nuevo. Esto permite que la base de datos se mantenga actualizada y precisa gracias a la participación de la comunidad de usuarios. Adicionalmente, los usuarios pueden calificar películas y programas de televisión, lo que ayuda a generar puntuaciones que reflejan la opinión general de la comunidad sobre un título en particular.

Además de ser un sitio web para consumidores, TMDb proporciona una API que permite a los desarrolladores acceder a su vasta base de datos para crear aplicaciones, sitios web y servicios relacionados con el entretenimiento.
Para poder acceder a la API se necesita registrar en la plataforma, obteniendo una llave o token. La llave se obtiene de manera gratuita, previa autorización de la plataforma. La documentación de la API tambiémn se puede revisar en el link a su sitio, accediendo a MORE -> API.

![image](https://github.com/Thiago-whatever/ProyectoFinal_NoSQL/assets/85588937/269105d2-5330-47eb-8671-2623f43b1703)


## Inicialización del proyecto
Para que se pueda correr este proyecto en cualquier computadora se deberá tener instalado previamente [Docker](https://www.docker.com/get-started/) y se deberán seguir las siguientes instrucciones:
+ Clonar este repositorio;
+ asegurarse que el daemon de docker esté corriendo;
+ posicionarse en la carpeta del repositorio recién clonado y correr el archivo 'movie_app.ipynb';
+ + es en este archivo donde se hace el ejecuta el Docker-Compose, el cual carga los contenedores, hace la conexión con la API, te conecta con el resto de las bases de datos y hace los queries.
+ como el proceso involucra descargar y procesar muchos datos de la API, así como transformarlos y cargarlos en MongoDB, Cassandra y Neo4j, se debe esperar alrededor de 5 minutos para que se garantice el correcto funcionamiento de todo el proyecto.
Los queries que se pueden hacer para las distintas bases de datos se deben correr en la terminal y se pueden encontrar en la carpeta [Queries](https://github.com/Thiago-whatever/ProyectoFinal_NoSQL/tree/main/Queries) de este repositorio.

## MongoDB
Para pasar los datos de la API a MongoDB se elaboró un script de python. En este script se hace la conexión tanto a la API como a MongoDB. Ahora, como se encontró que con el url en terminación '/discover/movie' las respuestas a los requests no tenían suficiente información para la elaboración del proyecto, se usa ese request para conseguir los ids de las películas y hacer otro request a otro url. Se optó, para no poblar demás la base de datos, por escoger el top 20 de películas más populares de cada año (1990-2024)

```python
url = f"{base_url}/movie/{id}?language=en-US"
        response = requests.get(url, headers=headers)
        results = response.json()
        if results:
            insert_Mongo(movies_collection, results)

```
Se optó por tener dos colecciones: "movies" y "credits". Para hacer manejo de esto, se tiene un método distinto para descargar los datos correspondientes a credits, y se muestra a continuación:

```python
url = f"{base_url}/movie/{id}/credits?language=en-US"
        response = requests.get(url, headers=headers)
        results = response.json()
        if results:
            insert_Mongo(credits_collection, results)
```

Por último cabe destacar el método 'insert_Mongo' el cual nos ayudó a poblar las distintas colecciones con los distintos sets de datos: 
```python
def insert_Mongo(collection, data):
    collection.insert_one(data)
```

Vale la pena que veamos cómo se ven los response de los dos distintos requests. Para el request de películas, con el cual poblamos la colección "movies" el response se veía de la siguiente forma: 

```json
{"_id":{"$oid":"656848b139c28fac6b06808b"},
"adult":false,"backdrop_path":"/sw7mordbZxgITU877yTpZCud90M.jpg",
"belongs_to_collection":null,
"budget":25000000,
"genres":[{"id":18,"name":"Drama"},{"id":80,"name":"Crime"}],
"homepage":"http://www.warnerbros.com/goodfellas",
"id":769,"imdb_id":"tt0099685",
"original_language":"en",
"original_title":"GoodFellas",
"overview":"The true story of Henry Hill, a half-Irish, half-Sicilian Brooklyn kid who is adopted by neighbourhood gangsters at an early age and climbs the ranks of a Mafia family under the guidance of Jimmy Conway.",
"popularity":85.372,
"poster_path":"/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
"production_companies":[{"id":8880,"logo_path":"/fE7LBw7Jz8R29EABFGCvWNriZxN.png","name":"Winkler Films",
"origin_country":"US"}],
"production_countries":[{"iso_3166_1":"US","name":"United States of America"}],
"release_date":"1990-09-12",
"revenue":46835000,
"runtime":145,
"spoken_languages":[{"english_name":"Italian","iso_639_1":"it","name":"Italiano"},{"english_name":"English","iso_639_1":"en","name":"English"}],
"status":"Released",
"tagline":"Three decades of life in the mafia.",
"title":"GoodFellas",
"video":false,
"vote_average":8.466,
"vote_count":11921}
```

Una parte del response que obtuvimos para créditos (no se puede incluir todo pues el documento es demasiado largo, el cast es muy grande para cada película) se muestra a continuación:
```json
{
  "id": 769,
  "cast": [
    {
      "adult": false,
      "gender": 2,
      "id": 11477,
      "known_for_department": "Acting",
      "name": "Ray Liotta",
      "original_name": "Ray Liotta",
      "popularity": 33.296,
      "profile_path": "/iXKotiB0Xe9iJLCBbjAedHPLb7p.jpg",
      "cast_id": 17,
      "character": "Henry Hill",
      "credit_id": "52fe4274c3a36847f801fd1f",
      "order": 0
    }
...
```

## Cassandra
Para hacer el proceso de ETL de MongoDB a Cassandra, se involucraron varios pasos, los cuales veremos a continuación.
Además de hacer la conexión, se hace un find({}) para cada una de las colecciones que tenemos. Cabe mencionar que de manera previa, se define el keyspace en Cassandra para poder trabajar: "mov" es el keyspace que se usa, pero se checa que no exista ningún keyspace con ese nombre; en caso de que exista se usará dicho keyspace.
```python
#Creation of keyspace
keyspace_name = "mov"

existing_keyspaces = cluster.metadata.keyspaces
if keyspace_name not in existing_keyspaces:
    session.execute(f"CREATE KEYSPACE {keyspace_name} WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': 1 }};")
```

Luego se generan las dos tablas sobre las cuales hacemos consultas:
```python
#Table creation
create_movie_cast_query = """
    CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id INT,
        cast_id INT,
        gender INT,
        name TEXT,
        character TEXT,
        popularity FLOAT,
        known_for_department TEXT,
        PRIMARY KEY (movie_id, cast_id, name)
    )
"""


create_movies_query = """
    CREATE TABLE IF NOT EXISTS movies (
        movie_id INT,
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
        spoken_languages SET<TEXT>,
        PRIMARY KEY (movie_id, popularity)
    )
"""
```
Finalmente con ayuda de un cursor, se extrae la información de MongoDB, se hace la transformación (tomamos las partes de los documentos json que queremos) y cargamos nuestras tablas en Cassandra. El siguiente fragmento de código, hace esto:

```python
#Funcion to insert data in movies table
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
```

## Neo4j
Para hacer el proceso de ETL de MongoDB a Neo4j, se involucraron varios pasos, los cuales veremos a continuación. Primero, se genera la conexión a ambas bases de datos. Para la transformación se saca toda la información de ambas colecciones con ayuda de un cursor, el cual será procesado con ayuda de la librería de pandas de python.

```python
#Get data from mongo
cursor = mongo_collection.find()
df = pd.DataFrame(list(cursor))
```
 El procesamiento para volver los datos del cursor un grafo se hace a continuación:

 ```python
#title,genre, release_date df
df.drop(columns=['_id','adult', 'backdrop_path', 'belongs_to_collection', 'budget', 'homepage','status', 
                        'tagline', 'video', 'vote_average', 'vote_count','imdb_id', 'original_language', 'original_title',
                        'overview', 'popularity', 'poster_path', 'revenue'], inplace=True)
df_normalized = df.explode('genres')
df_normalized['genres'] = df_normalized['genres'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
df_genero = df_normalized[['id','genres','title','release_date']]
df_genero['release_date'] = pd.to_datetime(df_genero['release_date'], format='%Y-%m-%d', errors='coerce')
```
Finalmente se genera el grafo y se sube a Neo4j
```python
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
```



# Disclaimer:

"This applicacion uses TMDB and the TMDB APIs but is not endorsed, certified, or otherwise approved by TMDB."
