from base64 import b64encode


class BookConsts:
    CATEGORIES: tuple[str, ...] = (
        'Science & Math', 'Education & Teaching', 'Computers & Technology', 'Classics', 'Adventure stories', 'Crime',
        'Fairy tales', 'Fantasy', 'Historical fiction', 'Horror', 'Humour and satire', 'Literary fiction', 'Mystery',
        'Poetry', 'Plays', 'Science fiction', 'Short stories', 'Thrillers', 'War', 'Autobiography', 'Biography'
    )


class Book:
    def __init__(self, book_id: int, name: str, author: str, category: int, image: bytes, date: str):
        self.book_id: int = book_id
        self.name: str = name
        self.author: str = author
        self.category_id: int = category
        self.category: str = BookConsts.CATEGORIES[self.category_id]
        self.image: str = b64encode(image).decode('utf-8')
        self.date: str = date

    @property
    def strip_category_name(self) -> str:
        if len(category_name := self.category) > 18:
            category_name = f'{category_name[:15]}...'
        return category_name

    @property
    def strip_author_name(self) -> str:
        if len(author_name := self.author) > 15:
            author_name = f'{author_name[:12]}...'
        return author_name

    def __str__(self) -> str:
        return f'<Book (name={self.name}, author={self.author}, category={self.category}, date={self.date})>'
