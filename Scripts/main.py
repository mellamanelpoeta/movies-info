import subprocess
from pymongo import MongoClient
from cassandra.cluster import Cluster
from neo4j import GraphDatabase

#Run the corresponging scripts
def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_name}: {e}")


if __name__ == "__main__":
        scripts_to_run = [
            "api_mongo_transfer.py",
            "mongo_cassandra_transfer.py",
            "mongo_neo4j_transfer.py"
        ]