
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass

    @abstractmethod
    def get_latest_data(self):
        pass