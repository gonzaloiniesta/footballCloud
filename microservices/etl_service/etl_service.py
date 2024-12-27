from integrations import MessagingQueueFactory, DataTransformer, StorageDataFactory

QUEUE_TYPE = 'Kafka'
KAFKA_URL = "localhost"
KAFKA_PORT = 9092
KAFKA_TOPIC = "player_stats"
CONSUMER_GROUP = "micro3"

DB_TYPE = "mongodb"
DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "footballcloud_db"
DB_USER = "admin"
DB_PASSWORD = "adminpassword"

STATS_TYPE = "player" # player or team
 


if __name__ == "__main__":

    consumer = MessagingQueueFactory(queue_type=QUEUE_TYPE,
                                     url=KAFKA_URL,
                                     port=KAFKA_PORT,
                                     topic=KAFKA_TOPIC,
                                     consumer_group=CONSUMER_GROUP)
    
    db = StorageDataFactory(storage_type=DB_TYPE,
                            url=DB_HOST, port=DB_PORT,
                            database_name=DB_NAME,
                            db_user=DB_USER,
                            db_password=DB_PASSWORD).create()

    trasformer = DataTransformer()

    for k, v in consumer.create().subscribe():
        data = trasformer.transform(k, v)
        if STATS_TYPE == 'player':
            db.process_player_statistics(k, data)
        else:
            db.process_team_statistics(k, data)
