from abc import ABC, abstractmethod

class ConsumerBrokerInterface(ABC):
    @abstractmethod
    def subscribe(self, callback):
        """
        Subscribe to a topic and process incoming messages using a callback.
        """
        pass