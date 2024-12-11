import json
from integrations import KafkaConsumerFootballCloud
import time

USERNAME = "admin"
PASSWORD = "adminpassword"
HOST = "localhost"
PORT = 27017
DB_NAME = "football_analytics"
KAFKA_URL = "localhost"
KAFKA_PORT = 9092

if __name__ == "__main__":
    consumer = KafkaConsumerFootballCloud(kafka_url=KAFKA_URL, kafka_port=KAFKA_PORT, topic="league_stats")

    consumer.subscribe()