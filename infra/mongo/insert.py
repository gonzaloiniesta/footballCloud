from pymongo import MongoClient
import json

client = MongoClient("mongodb://admin:adminpassword@localhost:27017/")
db = client['footballcloud_db']

json_file_path = "dml_mongodb.json"

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

for collection_name, documents in data.items():
    collection = db[collection_name]
    if isinstance(documents, list):
        if documents:
            collection.insert_many(documents)
            print(f"Inserted {len(documents)} documents into the '{collection_name}' collection.")
        else:
            collection.insert_one({"_placeholder": True})
            collection.delete_one({"_placeholder": True})
            print(f"The collection '{collection_name}' has been created as empty.")
    else:
        print(f"The value for '{collection_name}' is not a list and will be skipped.")

print("Data successfully loaded into MongoDB.")
