from abc import ABC, abstractmethod

class DataStorageInterface(ABC):
    @abstractmethod
    def connect(self):
        """
        Connect to the data storage.
        """
        pass

    @abstractmethod
    def insert(self, collection: str, data: dict):
        """
        Insert a document into the specified collection.
        """
        pass

    @abstractmethod
    def find(self, collection: str, query: dict):
        """
        Find documents in the specified collection matching the query.
        """
        pass

    @abstractmethod
    def update(self, collection: str, query: dict, new_values: dict):
        """
        Update documents in the specified collection matching the query.
        """
        pass

    @abstractmethod
    def delete(self, collection: str, query: dict):
        """
        Delete documents in the specified collection matching the query.
        """
        pass
