from io import StringIO
from bson import Binary
from typing import NoReturn
from src.logger import Logger
from src.db import DB, database
from src.modules.tools import strftime
from src.modules.web import set_cookies
from src.consts.routes import ApiRoutes
from src.modules.hashes import HASH, sha256
from src.modules.decorators import check_params
from aiohttp.web import Request, Response, HTTPFound
from src.consts.exceptions import NotFound, DataError
from src.db.interaction import UserInteraction, BookInteraction


class ApiHandler:
    def __init__(self):
        self.database: DB = database
        self.logger: Logger = Logger(name='ApiHandler')
        self.user_interaction: UserInteraction = UserInteraction()
        self.book_interaction: BookInteraction = BookInteraction()

    @check_params(params=['login', 'password'])
    async def login(self, login: str, password: str) -> HTTPFound:
        password_hash: HASH = await sha256(string=password)
        user_id, role, session, timestamp = await self.user_interaction.login(
            login=login,
            password_hash=password_hash
        )
        cookies: dict = {
            'id': user_id,
            'role': role,
            'login': login,
            'session': session,
            'registration_date': strftime(timestamp)
        }
        redirect: HTTPFound = HTTPFound(location='/')
        await set_cookies(redirect=redirect, cookies=cookies)
        return redirect

    @check_params(params=['login', 'password', 'role'])
    async def create_user(self, login: str, password: str, role: str) -> HTTPFound | NoReturn:
        if not await self.user_interaction.is_unique_login(login=login):
            raise DataError('This login already exists')
        password_hash: HASH = await sha256(string=password)
        user_id, session, timestamp = await self.user_interaction.create_user(
            login=login,
            password_hash=password_hash,
            role=role
        )
        cookies: dict = {
            'id': user_id,
            'role': role,
            'login': login,
            'session': session,
            'registration_date': strftime(timestamp)
        }
        redirect: HTTPFound = HTTPFound(location='/')
        await set_cookies(redirect=redirect, cookies=cookies)
        return redirect

    async def add_book(self, data: dict) -> Response | NoReturn:
        try:
            image = data['image']['content']
            binary_image: Binary = Binary(data=image)
            book_id, timestamp = await self.book_interaction.add_book(
                name=data['name'],
                author=data['author'],
                category=int(data['category']),
                image=binary_image
            )
            self.logger.info(
                text=f"Add new book | name: {data['name']} | author: {data['author']} | category: {data['category']} | "
                     f"book_id: {book_id} | timestamp: {timestamp}"
            )
            return HTTPFound(location='/')
        except Exception as exc:
            self.logger.exception(exc=exc)
            return Response(text=str(data))

    async def take_return_book(self, request: Request, data: dict, status: str) -> HTTPFound | NoReturn:
        if not (book_id := int(data.get('id', 0))):
            raise DataError('Wrong API params')
        user_id: int = int(request.cookies.get('id'))
        await self.book_interaction.take_return_book(user_id=user_id, book_id=book_id, status=status)
        return HTTPFound(location=f'/book?id={book_id}')

    async def statistics_book(self, data: dict) -> Response | NoReturn:
        if not (book_id := int(data.get('id', 0))) or not \
                await self.book_interaction.get_book_statistic(book_id=book_id):
            raise DataError('Wrong API params')
        csvfile: StringIO = await self.book_interaction.get_book_statistic_csv(book_id=book_id)
        response: Response = Response(
            body=csvfile.read(),
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="book_statistic_{book_id}.csv"'}
        )
        return response

    async def handler(self, request: Request, path: str, data: dict) -> Response | NoReturn:
        match path:
            case ApiRoutes.LOGIN:
                return await self.login(data=data)
            case ApiRoutes.CREATE_USER:
                return await self.create_user(data=data)
            case ApiRoutes.ADD_BOOK:
                return await self.add_book(data=data)
            case ApiRoutes.TAKE_BOOK:
                return await self.take_return_book(request=request, data=data, status='take')
            case ApiRoutes.RETURN_BOOK:
                return await self.take_return_book(request=request, data=data, status='return')
            case ApiRoutes.STATISTICS_BOOK:
                return await self.statistics_book(data=data)
            case _:
                print(request, path, data)
                raise NotFound

    async def __call__(self, request: Request, path: str, data: dict) -> Response:
        return await self.handler(request=request, path=path, data=data)
