from io import StringIO
from bson import Binary
from csv import DictWriter
from src.db import DB, database
from src.consts.book import Book
from typing import Optional, NoReturn
from pymongo.collection import Collection
from src.modules.tools import get_timestamp, strftime


class BookInteraction:
    def __init__(self):
        self.database: DB = database
        self.books: Collection = self.database.books

    async def add_book(self, name: str, author: str, category: int, image: Binary) -> tuple[int, float]:
        count: int = self.books.count_documents(filter={})
        book_id: int = count + 1
        timestamp: float = get_timestamp()
        document: dict = {
            '_id': book_id,
            'name': name,
            'author': author,
            'category': category,
            'image': image,
            'timestamp': timestamp
        }
        self.books.insert_one(document=document)
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

    async def take_return_book(self, user_id: int, book_id: int, status: str) -> NoReturn:
        book_statistics: Collection = self.database[f'book-statistics-{book_id}']
        document: dict = {
            '_id': book_statistics.count_documents(filter={}) + 1,
            'user_id': user_id,
            'status': status,
            'timestamp': get_timestamp()
        }
        book_statistics.insert_one(document=document)

    async def get_book_status(self, user_id: int, book_id: int) -> str:
        book_statistics: Collection = self.database[f'book-statistics-{book_id}']
        statistic: dict = book_statistics.find_one(filter={'user_id': user_id}, sort=[('_id', -1)]) or {}
        return statistic.get('status', 'return')

    async def get_book_statistic(self, book_id: int) -> dict:
        book_statistics: list[dict] = list(self.database[f'book-statistics-{book_id}'].find() or [])
        statistic: dict = {}
        for book_statistic in book_statistics:
            status_name: str = book_statistic['status']
            statistic[status_name]: int = statistic.get(status_name, 0) + 1
        return statistic

    async def get_book_statistic_csv(self, book_id: int) -> StringIO:
        book_statistics_collection: Collection = self.database[f'book-statistics-{book_id}']
        book_statistics = book_statistics_collection.find({})
        csv_headers: list[str] = ['USER ID', 'STATUS', 'DATE']
        csvfile: StringIO = StringIO()
        writer: DictWriter = DictWriter(f=csvfile, fieldnames=csv_headers)
        writer.writeheader()
        for item in book_statistics:
            writer.writerow(
                rowdict={
                    'USER ID': item['user_id'],
                    'STATUS': item['status'],
                    'DATE': strftime(timestamp=item['timestamp']),
                }
            )
        csvfile.seek(0)
        return csvfile
