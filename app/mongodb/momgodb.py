from pymongo import MongoClient
from typing import Generator

class MongoDB:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "football_analytics"):
        self.uri = uri
        self.db_name = db_name

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
