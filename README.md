# ProyectoFinal_NoSQL
Proyecto en el que se demuestra el entendimiento y capacidad de manejo de las diferentes bases de datos que vimos en el semestre, así como los conceptos relacionados con API’s, ETL’s, etc.
El objetivo del proyecto es integrar los siguientes elementos:
** Realizar solicitudes a una API de nuestra elección;
** insertar las respuestas a las solicitudes a una base de datos en MongoDB, la cual funcionará como DataLake;
** del DataLake se deberá poder hacer consultas y un proceso de extracción, transformación y carga a otras dos bases de datos: Cassandra y Neo4j;
** incorporar todos los elementos dentro de un Docker-Compose.

A lo largo de este documento se explicará la API que se escogió, cómo funciona el proyecto, los requisitos para su ejecución en cualquier entorno local y algunas consultas para cada una de las bases de datos, junto con la explicación de los resultados que arrojan. 

## Acerca de la API: TMDB - The Movie Database API
[The Movie Database (TMDB)](https://www.themoviedb.org/) es una base de datos en línea que contiene una amplia gama de información sobre películas y programas de televisión. Ofrece detalles como el elenco, equipo de producción, fechas de estreno, sinopsis, clasificaciones, puntuaciones de usuarios y críticos, imágenes, tráilers, posters y entre otros. En la plataforma, los usuarios pueden contribuir agregando información, corrigiendo errores o añadiendo contenido nuevo. Esto permite que la base de datos se mantenga actualizada y precisa gracias a la participación de la comunidad de usuarios. Adicionalmente, los usuarios pueden calificar películas y programas de televisión, lo que ayuda a generar puntuaciones que reflejan la opinión general de la comunidad sobre un título en particular.

Además de ser un sitio web para consumidores, TMDb proporciona una API que permite a los desarrolladores acceder a su vasta base de datos para crear aplicaciones, sitios web y servicios relacionados con el entretenimiento.
Para poder acceder a la API se necesita registrar en la plataforma, obteniendo una llave o token. La llave se obtiene de manera gratuita, previa autorización de la plataforma. La documentación de la API tambiémn se puede revisar en el link a su sitio, accediendo a MORE -> API.

"This applicacion uses TMDB and the TMDB APIs but is not endorsed, certified, or otherwise approved by TMDB."
