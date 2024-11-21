from pymongo import MongoClient, errors
from typing import Generator
import json


class MongoDB:
    def __init__(self, uri="mongodb://admin:adminpassword@localhost:27017/", db_name="football_analytics"):
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

    def get_data(self, collection_name: str, query: dict = None, projection: dict = None) -> list:
        """
        Retrieves data from a specified collection in the database.

        Parameters:
        - collection_name (str): The name of the collection to query.
        - query (dict): The query filter to apply (default is None, which retrieves all documents).
        - projection (dict): The fields to include or exclude (default is None, which includes all fields).

        Returns:
        - list: A list of documents matching the query.
        """
        if query is None:
            query = {}

        collection = self.db[collection_name]

        try:
            result = list(collection.find(query, projection))
            print(f"Successfully retrieved data from collection '{collection_name}'.")
            return result
        except Exception as e:
            print(f"An error occurred while retrieving data: {e}")
            return []

