from typing import List
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
        print("\n\nConnected to MongoDB Client!  Ping - ",self.client.admin.command('ping'),"\n\n ")

    def close(self):
        print("\n\n Closing MongoDB client connection \n\n")
        self.client.close()

    def insert(self, product: Product):
        return self.collection.insert_one(product.to_dict())

    #data type of products is List[Product]
    def update(self, product:Product):
        return self.collection.find_one_and_update({"product_title":product.product_title}, {"$set":{"product_price": product.product_price}}, {"new": True})
    
    def fetchOne(self, product_title: str):
        search ={"product_title":product_title}
        return self.collection.find_one(search)