import psycopg2
from psycopg2 import sql, extras
from typing import List, Dict, Any, Generator
import json

class PostgreSQLFootballCloud:

    def __init__(self, host="localhost", database="footballcloud_db", user="user", password="1234", port=5432):
        self.connection_params = {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
            "port": port,
        }
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.connection.autocommit = True
            print("✅ Successfully connected to PostgreSQL.")
        except psycopg2.Error as e:
            print(f"❌ Failed to connect to PostgreSQL: {e}")
            raise


    def get_team_id(self, team_name: str) -> int:
        """
        Retrieve the team_id for the given team name. If not found, insert the team.
        """
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT team_id FROM teams WHERE name = %s;"
                cursor.execute(query, (team_name,))
                result = cursor.fetchone()

                if result:
                    return result[0]

                # Insert the team if not found
                insert_query = "INSERT INTO teams (name) VALUES (%s) RETURNING team_id;"
                cursor.execute(insert_query, (team_name,))
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            print(f"❌ Error retrieving or inserting team '{team_name}': {e}")
            raise

    def get_player_id(self, player_name: str, team_name: str) -> int:
        """
        Retrieve the player_id for the given player name and team. If not found, insert the player.
        """
        try:
            team_id = self.get_team_id(team_name)

            with self.connection.cursor() as cursor:
                query = "SELECT player_id FROM players WHERE name = %s AND team_id = %s;"
                cursor.execute(query, (player_name, team_id))
                result = cursor.fetchone()

                if result:
                    return result[0]

                # Insert the player if not found
                insert_query = "INSERT INTO players (name, team_id) VALUES (%s, %s) RETURNING player_id;"
                cursor.execute(insert_query, (player_name, team_id))
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            print(f"❌ Error retrieving or inserting player '{player_name}': {e}")
            raise

    def insert_statistics(self, table_name: str, id_name: str, entity_id: int, data: Dict[str, Any]) -> None:
        """
        Insert statistics into the specified table.

        Parameters:
        - table_name (str): The name of the table.
        - id_name (str): The name of the ID column (team_id or player_id).
        - entity_id (int): The ID of the team or player.
        - data (dict): The statistics data to insert.
        """
        try:
            with self.connection.cursor() as cursor:
                columns = list(data.keys())
                values = list(data.values())
                placeholders = ", ".join(["%s"] * len(columns))

                query = sql.SQL("INSERT INTO {} ({}, {}) VALUES (%s, {})").format(
                    sql.Identifier(table_name),
                    sql.Identifier(id_name),
                    sql.SQL(", ").join(map(sql.Identifier, columns)),
                    sql.SQL(placeholders),
                )
                cursor.execute(query, [entity_id] + values)
                print(f"✅ Statistics inserted into '{table_name}' for {id_name}={entity_id}.")
        except psycopg2.Error as e:
            print(f"❌ Error inserting statistics into '{table_name}': {e}")
            raise

    def process_player_statistics(self, key: Dict[str, Any], value: Dict[str, Any]) -> None:
        """
        Process and insert player statistics based on the key and value.

        Parameters:
        - key (dict): Key containing 'player' and 'stats' type.
        - value (dict): The statistics data.
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
            print(f"⚠️ Unknown statistics type: {key['stats']} for player '{player_name}'.")

    def process_team_statistics(self, key: Dict[str, Any], value: Dict[str, Any]) -> None:
        """
        Process and insert team statistics based on the key and value.

        Parameters:
        - key (dict): Key containing 'team' and 'stats' type.
        - value (dict): The statistics data.
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
            print(f"⚠️ Unknown statistics type: {key['stats']} for team '{team_name}'.")

