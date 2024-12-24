from integrations import MessagingQueueFactory, DataTransformer, PostgreSQLFootballCloud

QUEUE_TYPE = 'Kafka'
USERNAME = "admin"
PASSWORD = "adminpassword"
HOST = "localhost"
PORT = 27017
DB_NAME = "football_analytics"
KAFKA_URL = "localhost"
KAFKA_PORT = 9092

if __name__ == "__main__":

    db = PostgreSQLFootballCloud()
    trasformer = DataTransformer()
    consumer = MessagingQueueFactory(queue_type=QUEUE_TYPE, url=KAFKA_URL, port=KAFKA_PORT, topic="player_stats", consumer_group="teams_etl")
    for k, v in consumer.create().subscribe():
        data = trasformer.transform(k, v)
        # db.process_team_statistics(k, data)
        # db.process_player_statistics(k, data)
        print(data['name'],",",data['team'])