from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

class KafkaProducerFootballCloud:
    def __init__(self, kafka_url, kafka_port, topic):
        """
        Constructor for KafkaProducerClass.

        :param kafka_url: The URL of the Kafka server.
        :param kafka_port: The port of the Kafka server.
        :param topic: The Kafka topic to which messages will be sent.
        """
        self.bootstrap_servers = f"{kafka_url}:{kafka_port}"
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def publish(self, message):
        """
        Publishes a message to the topic.

        :param message: The message to publish (must be JSON-serializable).
        """
        future = self.producer.send(self.topic, message)
        try:
            record_metadata = future.get(timeout=10)
            print(f"Message sent to {record_metadata.topic} [{record_metadata.partition}]")
        except KafkaError as e:
            print(f"Error sending the message: {e}")

