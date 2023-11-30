#!/bin/bash

docker-compose up -d --build
docker exec -it movies_app sh 
