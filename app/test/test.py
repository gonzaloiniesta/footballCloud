import json
import pandas as pd

# Ruta del archivo JSON
json_path = "/Users/giniest/FootballAnalytics/footballAnalytics/app/data/football_data.json"

# Cargar el archivo JSON completo
with open(json_path, "r") as f:
    data = json.load(f)

# Convertir las secciones específicas en DataFrames
players_df = pd.DataFrame(data["players"])
teams_df = pd.DataFrame(data["teams"])
matches_df = pd.DataFrame(data["matches"])

# Mostrar los DataFrames
print("Players DataFrame:")
print(players_df["total_goals"])

# print("\nTeams DataFrame:")
# print(teams_df)

# print("\nMatches DataFrame:")
# print(matches_df)