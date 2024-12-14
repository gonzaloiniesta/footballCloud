from integrations import MessagingQueueFactory

QUEUE_TYPE = 'Kafka'
USERNAME = "admin"
PASSWORD = "adminpassword"
HOST = "localhost"
PORT = 27017
DB_NAME = "football_analytics"
KAFKA_URL = "localhost"
KAFKA_PORT = 9092

if __name__ == "__main__":

    def imprime(k, v):
        print(f'Key: {k}, Value: {v}')

    consumer = MessagingQueueFactory(queue_type=QUEUE_TYPE, url=KAFKA_URL, port=KAFKA_PORT, topic="league_stats")
    consumer.create().subscribe(imprime)