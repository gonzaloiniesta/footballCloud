import json
import pandas as pd
from mongodb import MongoDB


db = MongoDB()

print(db.get_data("players"))
print("")
print(db.get_data("league"))
