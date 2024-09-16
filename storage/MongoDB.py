from typing import Any, List, Union
from models.Product import Product
from storage import StorageStrategy
import pymongo
import os

class MongoDBStrategy(StorageStrategy):
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        mongo_uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("DB_NAME")

        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db["products"]

    def insert(self, collection: str, data: Union[Product, Any]):
        if isinstance(data, Product):
            self.db[collection].insert_one(data.to_dict())
        self.db[collection].insert_one(data)

    #data type of products is List[Product]
    def bulk_insert(self, products:List[Product]):
        data = [product.to_dict() for product in products]
        self.collection.insert_many(data)