from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List

from models.Product import Product

class StorageStrategy(ABC):
    @abstractmethod
    def connect(self):
        pass

    def close(self):
        pass

    @abstractmethod
    def insert(self, product:Product)->Any:
        pass

    @abstractmethod
    def update(self, product: Product)->Any:
        pass

    @abstractmethod
    def fetchOne(self, product_title: str)->Any:
        pass