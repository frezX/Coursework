from bson import Binary
from typing import Optional
from src.db import DB, database
from src.consts.book import Book
from pymongo.collection import Collection
from src.modules.tools import get_timestamp, strftime


class BookInteraction:
    def __init__(self):
        self.database: DB = database
        self.books: Collection = self.database.books

    async def add_book(self, name: str, author: str, category: int, image: Binary) -> tuple[int, float]:
        count: int = self.books.count_documents({})
        book_id: int = count + 1
        timestamp: float = get_timestamp()
        book_data: dict = {
            '_id': book_id,
            'name': name,
            'author': author,
            'category': category,
            'image': image,
            'timestamp': timestamp
        }
        self.books.insert_one(document=book_data)
        return book_id, timestamp

    async def get_catalog(self) -> list[Book]:
        return [
            Book(
                book_id=book['_id'],
                name=book['name'],
                author=book['author'],
                category=book['category'],
                image=book['image'],
                date=strftime(timestamp=book['timestamp'])
            )
            for book in self.books.find()
        ]

    async def get_book(self, book_id: int) -> Optional[Book]:
        if not (book_data := self.books.find_one({'_id': book_id})):
            return
        book: Book = Book(
            book_id=book_id,
            name=book_data['name'],
            author=book_data['author'],
            category=book_data['category'],
            image=book_data['image'],
            date=strftime(timestamp=book_data['timestamp'])
        )
        return book
