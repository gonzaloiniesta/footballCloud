from abc import ABC, abstractmethod

class PublisherBrokerInterface(ABC):
    @abstractmethod
    def publish(self, key: dict, message: dict, topic: str):
        """
        Publish a message to a specific topic.
        """
        pass