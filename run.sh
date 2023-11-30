#!/bin/bash

# Detener y eliminar contenedores existentes (si los hay)
docker-compose down

# Construir y levantar los contenedores definidos en docker-compose.yml
docker-compose up --build
