from typing import NoReturn
from src.db import DB, database
from src.modules.tools import strftime
from src.modules.web import set_cookies
from src.consts.routes import ApiRoutes
from src.modules.hashes import HASH, sha256
from src.db.interaction import UserInteraction
from src.modules.decorators import check_params
from aiohttp.web import Request, Response, HTTPFound
from src.consts.exceptions import NotFound, DataError


class ApiHandler:
    def __init__(self):
        self.database: DB = database
        self.user_interaction: UserInteraction = UserInteraction()

    @check_params(params=['login', 'password'])
    async def login(self, login: str, password: str) -> Response:
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
    async def create_user(self, login: str, password: str, role: str) -> Response | NoReturn:
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

    async def handler(self, request: Request, path: str, data: dict) -> Response | NoReturn:
        match path:
            case ApiRoutes.LOGIN:
                return await self.login(data=data)
            case ApiRoutes.CREATE_USER:
                return await self.create_user(data=data)
            case _:
                print(request, path)
                raise NotFound

    async def __call__(self, request: Request, path: str, data: dict) -> Response:
        return await self.handler(request=request, path=path, data=data)
