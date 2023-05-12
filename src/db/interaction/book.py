from src.db import DB, database
from pymongo.collection import Collection


class BookInteraction:
    def __init__(self):
        self.database: DB = database
        self.books: Collection = self.database.books
