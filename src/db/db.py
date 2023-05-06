from src.env import db_env
from pymongo import MongoClient
from pymongo.database import Database
from env_attributes import Environment
from pymongo.collection import Collection


class DB:
    def __init__(self):
        self.env: Environment = db_env
        self.client: MongoClient = MongoClient(host=self.env.host, port=self.env.port)
        self.db: Database = self.client.database

    def __getattr__(self, collection: str) -> Collection:
        return self.db[collection]
