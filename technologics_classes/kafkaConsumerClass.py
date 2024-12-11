from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json

class KafkaConsumerFootballCloud:
    def __init__(self, kafka_url, kafka_port, topic, group_id='group_001'):
        """
        Constructor for KafkaConsumerClass.

        :param kafka_url: The URL of the Kafka server.
        :param kafka_port: The port of the Kafka server.
        :param topic: The Kafka topic to consume messages from.
        :param group_id: The consumer group identifier.
        """
        self.bootstrap_servers = f"{kafka_url}:{kafka_port}"
        self.topic = topic
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            # auto_offset_reset='earliest',
            group_id=group_id,
            # value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def subscribe(self):
        """
        Subscribes to the topic and consumes messages.
        """
        print(f"Listening for messages on topic '{self.topic}'...")
        try:
            for message in self.consumer:
                print(f"Message received: {message.key, message.value}")
        except KeyboardInterrupt:
            print("Subscription terminated by the user.")
