from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    db = client["football_analytics"]
    try:
        yield db
    finally:
        client.close()
