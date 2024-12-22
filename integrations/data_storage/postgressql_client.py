import psycopg2
from psycopg2 import sql, extras
from typing import List, Dict, Any, Generator
import json

class PostgreSQLFootballCloud:
    def __init__(self, host="localhost", database="footballcloud_db", user="user", password=1234, port=5432):
        """
        Initializes a connection to a PostgreSQL instance.

        Parameters:
        - host (str): The database host.
        - database (str): The name of the database to connect to.
        - user (str): The username for authentication.
        - password (str): The password for authentication.
        - port (int): The port number (default is 5432).
        """
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

    def get_connection(self) -> Generator:
        """
        Yields a database connection and ensures proper closure after use.
        """
        connection = psycopg2.connect(**self.connection_params)
        try:
            yield connection
        finally:
            connection.close()

    def insert(self, table_name: str, data: Dict[str, Any]) -> None:
        """
        Inserts a single record into the specified table.

        Parameters:
        - table_name (str): The name of the table.
        - data (dict): The record to insert.
        """
        try:
            with self.connection.cursor() as cursor:
                columns = sql.SQL(", ").join(map(sql.Identifier, data.keys()))
                values = sql.SQL(", ").join(sql.Placeholder() * len(data))
                query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table_name), columns, values
                )
                cursor.execute(query, tuple(data.values()))
                print(f"✅ Record inserted into '{table_name}'.")
        except psycopg2.Error as e:
            print(f"❌ Error inserting record: {e}")

    def insert_many(self, table_name: str, data: List[Dict[str, Any]]) -> None:
        """
        Inserts multiple records into the specified table.

        Parameters:
        - table_name (str): The name of the table.
        - data (list): A list of records to insert.
        """
        if not data:
            print("⚠️ No data to insert.")
            return

        try:
            with self.connection.cursor() as cursor:
                columns = data[0].keys()
                values = [[row[col] for col in columns] for row in data]
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
                extras.execute_values(cursor, query, values)
                print(f"✅ {len(data)} records inserted into '{table_name}'.")
        except psycopg2.Error as e:
            print(f"❌ Error inserting records: {e}")

    def find(self, table_name: str, query: str = "", params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Retrieves records from the specified table based on a query.

        Parameters:
        - table_name (str): The name of the table.
        - query (str): The WHERE clause for filtering (default is "").
        - params (tuple): The query parameters (default is an empty tuple).

        Returns:
        - list: A list of records.
        """
        try:
            with self.connection.cursor(cursor_factory=extras.DictCursor) as cursor:
                query = f"SELECT * FROM {table_name} {query}"
                cursor.execute(query, params)
                result = cursor.fetchall()
                print(f"✅ Retrieved {len(result)} records from '{table_name}'.")
                return [dict(row) for row in result]
        except psycopg2.Error as e:
            print(f"❌ Error retrieving records: {e}")
            return []

    def update(self, table_name: str, query: str, params: tuple, new_values: Dict[str, Any]) -> None:
        """
        Updates records in the specified table.

        Parameters:
        - table_name (str): The name of the table.
        - query (str): The WHERE clause for filtering.
        - params (tuple): The query parameters.
        - new_values (dict): The new values to set.
        """
        try:
            with self.connection.cursor() as cursor:
                set_clause = ", ".join(f"{key} = %s" for key in new_values.keys())
                final_query = f"UPDATE {table_name} SET {set_clause} {query}"
                cursor.execute(final_query, tuple(new_values.values()) + params)
                print(f"✅ Updated records in '{table_name}'.")
        except psycopg2.Error as e:
            print(f"❌ Error updating records: {e}")

    def delete(self, table_name: str, query: str, params: tuple) -> None:
        """
        Deletes records from the specified table.

        Parameters:
        - table_name (str): The name of the table.
        - query (str): The WHERE clause for filtering.
        - params (tuple): The query parameters.
        """
        try:
            with self.connection.cursor() as cursor:
                final_query = f"DELETE FROM {table_name} {query}"
                cursor.execute(final_query, params)
                print(f"✅ Deleted records from '{table_name}'.")
        except psycopg2.Error as e:
            print(f"❌ Error deleting records: {e}")

    def load_data_from_json(self, file_path: str) -> None:
        """
        Loads data from a JSON file and inserts it into the appropriate tables.

        Parameters:
        - file_path (str): Path to the JSON file containing the data.
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            self.insert_many("players", data.get("players", []))
            self.insert_many("teams", data.get("teams", []))
            self.insert("leagues", data.get("leagues", {}))
            self.insert_many("matches", data.get("matches", []))

            print("✅ Data successfully loaded from JSON file into PostgreSQL.")
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except Exception as e:
            print(f"❌ Error loading data from JSON: {e}")
