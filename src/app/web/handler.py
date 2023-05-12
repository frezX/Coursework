from typing import NoReturn
from src.consts import templates
from src.consts.web import WebConsts
from src.consts.routes import WebRoutes
from src.consts.exceptions import NotFound
from src.db.interaction import UserInteraction
from aiohttp.web import Response, Request, HTTPFound
from src.modules.web import render_template, del_cookies, validate_cookies


class WebHandler:
    def __init__(self):
        self.user_interaction: UserInteraction = UserInteraction()

    async def index(self, request: Request) -> tuple[str, dict] | NoReturn:
        cookies: dict = dict(request.cookies)
        if not cookies or not await validate_cookies(cookies=cookies, needed_cookies=WebConsts.NEEDED_COOKIES)\
                or not await self.user_interaction.verify_user_with_cookies(cookies=cookies):
            raise HTTPFound(location=f'/{WebRoutes.LOGIN}')
        params: dict = {
            'user_id': cookies['id'],
            'role': cookies['role'],
            'login': cookies['login'],
            'session': cookies['session'],
            'registration_date': cookies['registration_date'],
            'consts': {
                'roles_allowed_add_books': 'librarian, admin, teacher'
            }
        }
        return templates['index'], params

    @staticmethod
    async def default_route_handler(path: str, data: dict) -> tuple[str, dict]:
        params: dict = {
            'data': data
        }
        return templates[path], params

    @staticmethod
    async def logout() -> NoReturn:
        redirect: HTTPFound = HTTPFound(location=f'/{WebRoutes.LOGIN}')
        await del_cookies(redirect=redirect, cookies=WebConsts.NEEDED_COOKIES)
        raise redirect

    async def add_book(self, request: Request) -> tuple[str, dict] | NoReturn:
        cookies: dict = dict(request.cookies)
        if not cookies or not await validate_cookies(cookies=cookies, needed_cookies=WebConsts.NEEDED_COOKIES)\
                or not await self.user_interaction.verify_user_with_cookies(cookies=cookies):
            raise HTTPFound(location=f'/{WebRoutes.LOGIN}')
        if role := cookies['role'] not in WebConsts.ROLES_ALLOWED_ADD_BOOKS:
            raise HTTPFound(location=f'/{WebRoutes.INDEX}')
        params: dict = {
            'user_id': cookies['id'],
            'role': role,
            'consts': {
                'categories': WebConsts.BOOK_CONSTS.CATEGORIES
            }
        }
        return templates[WebRoutes.ADD_BOOK], params

    async def handler(self, request: Request, path: str, data: dict) -> tuple[str, dict] | NoReturn:
        match path:
            case WebRoutes.INDEX:
                return await self.index(request=request)
            case WebRoutes.LOGIN | WebRoutes.REGISTRATION:
                return await self.default_route_handler(path=path, data=data)
            case WebRoutes.ADD_BOOK:
                return await self.add_book(request=request)
            case WebRoutes.LOGOUT:
                await self.logout()
            case _:
                raise NotFound

    async def __call__(self, request: Request, path: str, data: dict) -> Response:
        try:
            template, params = await self.handler(request=request, path=path, data=data)
            return await render_template(request=request, template=template, params=params)
        except HTTPFound as redirect:
            return redirect
