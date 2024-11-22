import json
from pymongo import MongoClient
import time

USERNAME = "admin"
PASSWORD = "adminpassword"
HOST = "localhost"
PORT = 27017
DB_NAME = "football_analytics"

def connect_to_mongo():
    while True:
        try:
            client = MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?authSource=admin")
            db = client[DB_NAME]
            print("Connected to MongoDB successfully.")
            return db
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}. Retrying...")
            time.sleep(5)

def load_data(db):
    file_path = "football_data.json"
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        # Insertar datos en las colecciones
        db.players.insert_many(data["players"])
        db.teams.insert_many(data["teams"])
        db.league.insert_one(data["league"])
        db.matches.insert_many(data["matches"])

        print("Initial data loaded successfully into football_analytics")
    except Exception as e:
        print(f"An error occurred while loading data: {e}")

# Ejecutar el script
if __name__ == "__main__":
    db = connect_to_mongo()
    load_data(db)
