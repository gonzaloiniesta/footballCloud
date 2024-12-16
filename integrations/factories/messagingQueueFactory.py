from integrations import KafkaConsumerFootballCloud
import sys
import logging

logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

class MessagingQueueFactory:
    def __init__(self, queue_type, url: str, port: int, topic: str, consumer_group=None):
        self.queue_type = queue_type
        self.url = url
        self.port = port
        self.topic = topic
        self.consumer_group = consumer_group

    def create(self):
        if self.queue_type == 'rabbitmq':
            logging.error("RabbitMQ integration is not implemented yet.")
            sys.exit(1)
        elif self.queue_type == 'Kafka':
            if self.consumer_group is None:
                return KafkaConsumerFootballCloud(kafka_url=self.url, 
                                                kafka_port=self.port, 
                                                topic=self.topic,)
            else:
                return KafkaConsumerFootballCloud(kafka_url=self.url, 
                                                kafka_port=self.port, 
                                                topic=self.topic,
                                                group_id=self.consumer_group)

        else:
            raise ValueError(f"Messaging queue type '{self.queue_type}' is not supported.")
