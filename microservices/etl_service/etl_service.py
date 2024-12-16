from integrations import MessagingQueueFactory, DataTransformer

QUEUE_TYPE = 'Kafka'
USERNAME = "admin"
PASSWORD = "adminpassword"
HOST = "localhost"
PORT = 27017
DB_NAME = "football_analytics"
KAFKA_URL = "localhost"
KAFKA_PORT = 9092

if __name__ == "__main__":

    trasformer = DataTransformer()
    consumer = MessagingQueueFactory(queue_type=QUEUE_TYPE, url=KAFKA_URL, port=KAFKA_PORT, topic="league_stats", consumer_group="test1234")
    for k, v in consumer.create().subscribe():
        print("Transformado:")
        print(trasformer.transform(k, v))
