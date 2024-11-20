from pymongo import MongoClient
from typing import Generator


from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="football_analytics"):
        self.uri = uri
        self.db_name = db_name
        self.client = MongoClient(self.uri)
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

    def insert_document(self, collection_name: str, document: dict):
        """
        Inserta un documento en la colección especificada.
        """
        self.db[collection_name].insert_one(document)
        print(f"Documento insertado en la colección '{collection_name}'.")

    def insert_documents(self, collection_name: str, documents: list):
        """
        Inserta múltiples documentos en la colección especificada.
        """
        self.db[collection_name].insert_many(documents)
        print(f"{len(documents)} documentos insertados en la colección '{collection_name}'.")
