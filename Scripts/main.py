import subprocess

def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_name}: {e}")

if __name__ == "__main__":
    # Ejecutar en orden
    scripts_to_run = [
        "api_mongo_transfer.py",
        "mongo_cassandra_transfer.py",
        "mongo_neo4j_transfer.py"
    ]

    for script in scripts_to_run:
        run_script(script)