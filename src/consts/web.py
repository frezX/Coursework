from .book import BookConsts


class WebConsts:
    NEEDED_COOKIES: tuple[str, ...] = 'id', 'role', 'login', 'session', 'registration_date'
    ROLES_ALLOWED_ADD_BOOKS: tuple[str, ...] = 'librarian', 'teacher', 'admin'
    BOOK_CONSTS: BookConsts = BookConsts()
