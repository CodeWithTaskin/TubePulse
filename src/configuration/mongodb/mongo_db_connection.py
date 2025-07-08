import sys
from pymongo import MongoClient

from src.logging import logging
from src.exception import MyException


class MongoDBConnection:
    def __init__(self, db_name: str, collection_name: str, connection_url: str):
        try:
            logging.info('Connecting with MongoDB....')
            client = MongoClient(connection_url)
            status = client.admin.command('ping')
            if status['ok'] == 1:
                logging.info('MongoDB Connected Successfully....')
                database = client[db_name]
                self.collection = database[collection_name]
            else:
                logging.info('MongoDB Connection Failed....')
        except Exception as e:
            raise MyException(e, sys) from e
    
    def collection_entity(self):
        try:
            return self.collection
        except Exception as e:
            raise MyException(e, sys) from e