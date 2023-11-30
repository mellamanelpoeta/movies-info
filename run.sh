#!/bin/bash

cd Scripts
python -m venv moviesdb
source moviesdb/bin/activate
pip install -r requirements.txt

docker-compose up -d --build

code .
