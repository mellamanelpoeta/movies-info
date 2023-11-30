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

## Inicialización del proyecto
Para que se pueda correr este proyecto en cualquier computadora se deberá tener instalado previamente [Docker](https://www.docker.com/get-started/) y se deberán seguir las siguientes instrucciones:
+ Clonar este repositorio;
+ asegurarse que el daemon de docker esté corriendo;
+ posicionarse en la carpeta del repositorio recién clonado y correr el archivo run.sh en la terminal;
+ como el proceso involucra descargar y procesar muchos datos de la API, así como transformarlos y cargarlos en MongoDB, Cassandra y Neo4j, se debe esperar alrededor de 3 minutos para que se garantice el correcto funcionamiento de todo el proyecto.
+ para confirmar que los contenedores se crearon y están corriendo se puede correr el siguiente comando en la terminal:
```shell
docker ps
```
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
## Cassandra

## Neo4j

"This applicacion uses TMDB and the TMDB APIs but is not endorsed, certified, or otherwise approved by TMDB."
