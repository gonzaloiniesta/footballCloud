from kafka import KafkaConsumer
from kafka.errors import KafkaError
from integrations import ConsumerBrokerInterface
import json, sys

class KafkaConsumerFootballCloud(ConsumerBrokerInterface):
    def __init__(self, kafka_url, kafka_port, topic, group_id='group_001'):
        """
        Constructor for KafkaConsumerFootballCloud.

        :param kafka_url: The URL of the Kafka server.
        :param kafka_port: The port of the Kafka server.
        :param topic: The Kafka topic to consume messages from.
        :param group_id: The consumer group identifier.
        """
        self.bootstrap_servers = f"{kafka_url}:{kafka_port}"
        self.topic = topic

        try:
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                key_deserializer=lambda k: json.loads(k.decode('utf-8')) if k else None
            )

            print(f"✅ Successfully connected to Kafka at {self.bootstrap_servers}.")
        except KafkaError as e:
            print(f"❌ Failed to connect to Kafka: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ An unexpected error occurred while connecting to Kafka: {e}")
            sys.exit(1)

    def subscribe(self):
        """
        Subscribes to the topic and consumes messages.

        :param callback: A function to process each message received.
        """
        print(f"Listening for messages on topic '{self.topic}'...")
        try:
            for message in self.consumer:
              yield message.key, message.value
        except KeyboardInterrupt:
            print("❌ Subscription terminated by the user.")
        except KafkaError as e:
            print(f"❌ Error while consuming messages: {e}")
