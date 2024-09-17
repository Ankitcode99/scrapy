
import json
from typing import Any, List
from upstash_redis import Redis
import os

from models.Product import Product
from storage.StorageStrategy import StorageStrategy
from utils.productUtils import generate_id_from_product_title

class RedisStrategy(StorageStrategy):

    def __init__(self):
        self.client = None

    def connect(self):
        redis_url = os.getenv('UPSTASH_REDIS_URL');
        redis_token = os.getenv('UPSTASH_REDIS_TOKEN');
        self.client = Redis(url=redis_url, token=redis_token)
        print("\n\nConnected to Redis Client! Ping - ", self.client.ping(),"\n\n")
    
    def close(self):
        print("\n\n Closing Redis client connection \n\n")
        self.client.close()

    def insert(self, product:Product)->Any:
        return self.client.set(f"product:{generate_id_from_product_title(productTitle=product.product_title)}",value=json.dumps(product.to_dict()))

    def fetchOne(self, product_title: str)->Any:
        response:str = self.client.get(f"product:{generate_id_from_product_title(productTitle=product_title)}")
        if response:
            # Decode the byte string and convert it back to a dictionary
            retrieved_dict = json.loads(response)
            # print("Retrieved dict- ", retrieved_dict)
            return retrieved_dict # Output: {'var1': 5, 'var2': 9}
        else:
            return None

    def update(self, product: Product):
        return self.insert(product)