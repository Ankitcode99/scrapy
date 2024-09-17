
from typing import Any, List
from upstash_redis import Redis
import os

from models.Product import Product
from storage.StorageStrategy import StorageStrategy
from utils.productUtils import generateIdFromProductTitle

class RedisStrategy(StorageStrategy):

    def __init__(self):
        self.client = None

    def connect(self):
        redis_url = os.getenv('UPSTASH_REDIS_URL');
        redis_token = os.getenv('UPSTASH_REDIS_TOKEN');
        self.client = Redis(url=redis_url, token=redis_token)
        print("\n\nConnected to Redis Client! Ping - ", self.client.ping(),"\n\n")
    
    def close(self):
        self.client.close()

    def insert(self, product:Product)->Any:
        return self.client.set(f"product:{generateIdFromProductTitle(productTitle=product.product_title)}",value=product.to_dict())

    def fetchOne(self, product_title: str)->Any:
        return self.client.get(f"product:{generateIdFromProductTitle(productTitle=product_title)}")

    async def bulk_insert(self, products: List[Product]):
        pipe = self.client.pipeline()
        for product in products:
            pipe.hset(f"product:{product.id}", mapping=product.to_dict())
        pipe.execute()