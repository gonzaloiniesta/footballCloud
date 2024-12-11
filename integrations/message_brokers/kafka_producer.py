from kafka import KafkaProducer
from kafka.errors import KafkaError
from integrations import PublisherBrokerInterface
import json

class KafkaProducerFootballCloud(PublisherBrokerInterface):
    def __init__(self, kafka_url, kafka_port):
        """
        Constructor for KafkaProducerFootballCloud.

        :param kafka_url: The URL of the Kafka server.
        :param kafka_port: The port of the Kafka server.
        """
        self.bootstrap_servers = f"{kafka_url}:{kafka_port}"
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            key_serializer=lambda k: json.dumps(k).encode('utf-8'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def publish(self, key: dict, message: dict, topic: str):
        """
        Publishes a message to the Kafka topic.

        :param key: The key for the message (must be JSON-serializable).
        :param message: The message to publish (must be JSON-serializable).
        :param topic: The Kafka topic to which the message will be sent.
        """
        try:
            future = self.producer.send(topic=topic, key=key, value=message)
            record_metadata = future.get(timeout=10)
            print(f"📤 Message sent to topic: {record_metadata.topic}")
        except KafkaError as e:
            print(f"❌ Error sending the message: {e}")
