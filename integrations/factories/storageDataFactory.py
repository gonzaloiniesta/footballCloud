from integrations import PostgreSQLFootballCloud, MongoDBFootballCloud
import logging

logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

class StorageDataFactory:
    def __init__(self, storage_type, url: str, port: int, database_name: str, db_user: str, db_password: str):
        self.queue_type = storage_type
        self.url = url
        self.port = port
        self.database_name = database_name
        self.db_user = db_user
        self.db_password = db_password

    def create(self):
        if self.queue_type == 'mongodb':
            return MongoDBFootballCloud(uri=f'mongodb://{self.db_user}:{self.db_password}@{self.url}:{self.port}/',
                                        db_name=self.database_name)
        elif self.queue_type == 'postgress':
            return PostgreSQLFootballCloud(host=self.url,
                                           port=self.port,
                                           database=self.database_name,
                                           user=self.db_user,
                                           password=self.db_password)
        else:
            raise ValueError(f"Storage Data type '{self.queue_type}' is not supported.")
