from pymongo import MongoClient, errors
from typing import Generator
import json


class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="football_analytics"):
        """
        Initializes a connection to a MongoDB instance.

        Parameters:
        - uri (str): The MongoDB connection URI. Defaults to "mongodb://localhost:27017".
        - db_name (str): The name of the database to connect to. Defaults to "football_analytics".
        """
        self.uri = uri
        self.db_name = db_name

        try:
            self.client = MongoClient(self.uri)
            print("Successfully connected to MongoDB.")
        except errors.ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

        self.db = self.client[self.db_name]

    def get_db(self) -> Generator:
        """
        Yields a MongoDB database connection. Ensures the connection is closed after use.
        """
        client = MongoClient(self.uri)
        db = client[self.db_name]
        try:
            yield db
        finally:
            client.close()

    def load_data(self, data) -> None:
        """
        Loads all league information into the database from a JSON file.
        
        Parameters:
        - data: Path to the JSON file containing league data.
        """
        players_collection = self.db["players"]
        teams_collection = self.db["teams"]
        league_collection = self.db["league"]
        matches_collection = self.db["matches"]

        with open(data, "r") as f:
            data = json.load(f)

        
        players_collection.insert_many(data["players"])
        teams_collection.insert_many(data["teams"])
        league_collection.insert_one(data["league"])
        matches_collection.insert_many(data["matches"])

        print("Data successfully inserted into MongoDB.")
