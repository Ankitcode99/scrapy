from typing import Any, List, Union
from models.Product import Product

import pymongo
import os

from storage.StorageStrategy import StorageStrategy

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
        print("\n\nConnected to MongoDB Client!\n\n")

    def close(self):
        self.client.close()

    async def insert(self, product: Product):
        return await self.collection.insert_one(product.to_dict())

    #data type of products is List[Product]
    async def bulk_insert(self, products:List[Product]):
        data = [product.to_dict() for product in products]
        return await self.collection.insert_many(data)
    
    async def fetchOne(self, product_title: str):
        return await self.collection.find_one({product_title})