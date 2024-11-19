import pandas as pd
import json
from mongodb import MongoDB  # Asegúrate de tener la clase MongoDB definida como antes

class BusinessIntelligenceMethods:
    def __init__(self):
        # Inicializa una instancia de MongoDB
        self.mongo = MongoDB()

    def get_collection_as_dataframe(self, collection_name: str) -> pd.DataFrame:
        raise NotImplementedError("This method should be implemented by subclasses")

    def export_collection_to_json(self, collection_name: str, file_path: str):
        raise NotImplementedError("This method should be implemented by subclasses")

    def analyze_goals_by_team(self, collection_name: str) -> pd.DataFrame:
        raise NotImplementedError("This method should be implemented by subclasses")
