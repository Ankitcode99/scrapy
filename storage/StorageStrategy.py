from abc import ABC, abstractmethod

class StorageStrategy(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def insert(self, product):
        pass

    @abstractmethod
    def bulk_insert(self, products):
        pass