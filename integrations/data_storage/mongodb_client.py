from pymongo import MongoClient, errors
from integrations.interfaces.data_storage import DataStorageInterface
from typing import Generator, Any, Dict, List
import json

class MongoDBFootballCloud(DataStorageInterface):
    def __init__(self, uri: str = "mongodb://admin:adminpassword@localhost:27017/", db_name: str = "football_cloud"):
        """
        Initializes a connection to a MongoDB instance.

        Parameters:
        - uri (str): The MongoDB connection URI.
        - db_name (str): The name of the database to connect to.
        """
        self.uri = uri
        self.db_name = db_name

        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print("✅ Successfully connected to MongoDB.")
        except errors.ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise

    def get_db(self) -> Generator:
        """
        Yields a MongoDB database connection and closes it after use.
        """
        client = MongoClient(self.uri)
        db = client[self.db_name]
        try:
            yield db
        finally:
            client.close()

    def insert(self, collection_name: str, data: Dict[str, Any]) -> None:
        """
        Inserts a single document into the specified collection.

        Parameters:
        - collection_name (str): The name of the collection.
        - data (dict): The document to insert.
        """
        collection = self.db[collection_name]
        try:
            collection.insert_one(data)
            print(f"✅ Document inserted into '{collection_name}' collection.")
        except Exception as e:
            print(f"❌ Error inserting document: {e}")

    def insert_many(self, collection_name: str, data: List[Dict[str, Any]]) -> None:
        """
        Inserts multiple documents into the specified collection.

        Parameters:
        - collection_name (str): The name of the collection.
        - data (list): A list of documents to insert.
        """
        collection = self.db[collection_name]
        try:
            collection.insert_many(data)
            print(f"✅ {len(data)} documents inserted into '{collection_name}' collection.")
        except Exception as e:
            print(f"❌ Error inserting documents: {e}")

    def find(self, collection_name: str, query: Dict[str, Any] = None, projection: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Retrieves documents from the specified collection.

        Parameters:
        - collection_name (str): The name of the collection.
        - query (dict): The query filter to apply (default is None).
        - projection (dict): The fields to include/exclude (default is None).

        Returns:
        - list: A list of documents matching the query.
        """
        collection = self.db[collection_name]
        query = query or {}

        try:
            result = list(collection.find(query, projection))
            print(f"✅ Retrieved {len(result)} documents from '{collection_name}' collection.")
            return result
        except Exception as e:
            print(f"❌ Error retrieving documents: {e}")
            return []

    def update(self, collection_name: str, query: Dict[str, Any], new_values: Dict[str, Any]) -> None:
        """
        Updates documents in the specified collection.

        Parameters:
        - collection_name (str): The name of the collection.
        - query (dict): The filter to match documents.
        - new_values (dict): The new values to set.
        """
        collection = self.db[collection_name]
        try:
            result = collection.update_many(query, {"$set": new_values})
            print(f"✅ Updated {result.modified_count} documents in '{collection_name}' collection.")
        except Exception as e:
            print(f"❌ Error updating documents: {e}")

    def delete(self, collection_name: str, query: Dict[str, Any]) -> None:
        """
        Deletes documents from the specified collection.

        Parameters:
        - collection_name (str): The name of the collection.
        - query (dict): The filter to match documents to delete.
        """
        collection = self.db[collection_name]
        try:
            result = collection.delete_many(query)
            print(f"✅ Deleted {result.deleted_count} documents from '{collection_name}' collection.")
        except Exception as e:
            print(f"❌ Error deleting documents: {e}")

    def load_data_from_json(self, file_path: str) -> None:
        """
        Loads data from a JSON file and inserts it into the appropriate collections.

        Parameters:
        - file_path (str): Path to the JSON file containing the data.
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            self.insert_many("players", data.get("players", []))
            self.insert_many("teams", data.get("teams", []))
            self.insert("leagues", data.get("leagues", {}))
            self.insert_many("matches", data.get("matches", []))

            print("✅ Data successfully loaded from JSON file into MongoDB.")
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except Exception as e:
            print(f"❌ Error loading data from JSON: {e}")
