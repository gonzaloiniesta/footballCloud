from pymongo import MongoClient, errors
from typing import Generator, Any, Dict, List
import json

class MongoDBFootballCloud:

    def __init__(self, uri: str = "mongodb://admin:adminpassword@localhost:27017/",
                 db_name: str = "footballcloud_db"):
        """
        Initializes the connection to a MongoDB instance.
        """
        self.uri = uri
        self.db_name = db_name

        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print("✅ Successfully connected to MongoDB.")
        except errors.ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise

    def get_team_id(self, team_name: str) -> Any:
        """
        Retrieves the team ID by its name. If it does not exist, inserts it.
        """
        collection = self.db['teams']
        result = collection.find_one({"name": team_name})
        if result:
            return result["_id"]
        
        # Insert a new team if it does not exist
        new_team = {"name": team_name}
        insert_result = collection.insert_one(new_team)
        return insert_result.inserted_id

    def get_player_id(self, player_name: str, team_name: str) -> Any:
        """
        Retrieves the player ID by their name and team. If it does not exist, inserts it.
        """
        collection = self.db['players']
        team_id = self.get_team_id(team_name)
        result = collection.find_one({"name": player_name, "team_id": team_id})
        if result:
            return result["_id"]
        
        # Insert a new player if it does not exist
        new_player = {"name": player_name, "team_id": team_id}
        insert_result = collection.insert_one(new_player)
        return insert_result.inserted_id

    def insert_statistics(self, collection_name: str, id_name: str, entity_id: Any, data: Dict[str, Any]) -> None:
        """
        Inserts statistics into the specified collection. If they already exist, updates them.
        """
        collection = self.db[collection_name]
        try:
            collection.update_one(
                {id_name: entity_id},
                {"$set": data},
                upsert=True
            )
            print(f"✅ Statistics inserted or updated in '{collection_name}' for {id_name}={entity_id}.")
        except Exception as e:
            print(f"❌ Failed to insert or update statistics in '{collection_name}': {e}")

    def process_player_statistics(self, key: Dict[str, Any], value: Dict[str, Any]) -> None:
        """
        Processes and inserts player statistics.
        """
        player_name = value['name']
        team_name = value['team']
        player_id = self.get_player_id(player_name, team_name)

        table_map = {
            'Ataques': 'player_attack_statistics',
            'Disciplina': 'player_discipline_statistics',
            'Clasico': 'player_classic_statistics',
            'Defensiva': 'player_defensive_statistics',
            'Eficiencia': 'player_efficiency_statistics',
        }

        stats_table = table_map.get(key['stats'])
        if stats_table:
            self.insert_statistics(stats_table, 'player_id', player_id, value)
        else:
            print(f"Unknown statistics type: {key['stats']} for player '{player_name}'.")

    def process_team_statistics(self, key: Dict[str, Any], value: Dict[str, Any]) -> None:
        """
        Processes and inserts team statistics.
        """
        team_name = value['team']
        team_id = self.get_team_id(team_name)

        table_map = {
            'Ataques': 'attack_statistics',
            'Disciplina': 'discipline_statistics',
            'Clasico': 'classic_statistics',
            'Defensiva': 'defensive_statistics',
            'Eficiencia': 'efficiency_statistics',
        }

        stats_table = table_map.get(key['stats'])
        if stats_table:
            self.insert_statistics(stats_table, 'team_id', team_id, value)
        else:
            print(f"Unknown statistics type: {key['stats']} for team '{team_name}'.")

    def get_db(self) -> Generator:
        """
        Yields a MongoDB database connection.
        """
        client = MongoClient(self.uri)
        db = client[self.db_name]
        yield db
