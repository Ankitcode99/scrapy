
import os
from storage.MongoDB import MongoDBStrategy
from storage.Redis import RedisStrategy


class DatabaseClient:
    _instance = None

    def __new__(self):
        if self._instance is None:
            if( os.getenv('DATABASE') == 'REDIS'):
                self._instance = RedisStrategy()
            else:
                self._instance = MongoDBStrategy()

            self._instance.connect()
        return self._instance
