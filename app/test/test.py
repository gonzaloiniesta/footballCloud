import json
import pandas as pd
from mongodb import MongoDB

# Ruta del archivo JSON
json_path = "/home/gonzalo/footballAnalytics/app/data/football_data.json"

db = MongoDB()

db.load_data(json_path)

print(db.get_data("players"))
print("")
print(db.get_data("league"))
