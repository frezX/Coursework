class Templates:
    INDEX: str = 'index.html'
    LOGIN: str = 'login.html'
    REGISTRATION: str = 'registration.html'
    ADD_BOOK: str = 'add-book.html'
    BOOK: str = 'book.html'

    def __getitem__(self, item: str) -> str:
        return Templates.__getattribute__(self, item.upper())
