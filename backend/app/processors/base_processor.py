from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process_message(self, data):
        """Process incoming data."""
        pass

    @abstractmethod
    def get_latest_data(self) -> dict:
        """Retrieve the latest processed data as a dictionary."""
        pass