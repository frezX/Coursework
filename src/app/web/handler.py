from src.consts import templates
from typing import Optional, NoReturn
from src.consts.routes import WebRoutes
from src.consts.exceptions import NotFound
from src.db.interaction import UserInteraction
from aiohttp.web import Response, Request, HTTPFound
from src.modules.web import render_template, del_cookies, validate_cookies


class WebHandler:
    def __init__(self):
        self.needed_cookies: tuple[str, ...] = ('id', 'role', 'login', 'session')
        self.user_interaction: UserInteraction = UserInteraction()

    async def index(self, request: Request) -> tuple[str, dict] | NoReturn:
        cookies: dict = dict(request.cookies)
        if not cookies or not await validate_cookies(cookies=cookies, needed_cookies=self.needed_cookies):
            raise HTTPFound(location=f'/{WebRoutes.LOGIN}')
        user_id: int = int(cookies['id'])
        role: str = cookies['role']
        login: str = cookies['login']
        session: str = cookies['session']
        session_in_db: Optional[dict] = self.user_interaction.sessions.find_one(filter={'_id': user_id})
        if session_in_db and session_in_db.get('session') != session:
            raise HTTPFound(location=f'/{WebRoutes.LOGIN}')
        params: dict = {
            'user_id': user_id,
            'role': role,
            'login': login,
            'session': session
        }
        return templates['index'], params

    @staticmethod
    async def default_route_handler(path: str, data: dict) -> tuple[str, dict]:
        params: dict = {
            'data': data
        }
        return templates[path], params

    async def logout(self) -> NoReturn:
        redirect: HTTPFound = HTTPFound(location=f'/{WebRoutes.LOGIN}')
        await del_cookies(redirect=redirect, cookies=self.needed_cookies)
        raise redirect

    async def handler(self, request: Request, path: str, data: dict) -> tuple[str, dict] | NoReturn:
        match path:
            case WebRoutes.INDEX:
                return await self.index(request=request)
            case WebRoutes.LOGIN | WebRoutes.REGISTRATION:
                return await self.default_route_handler(path=path, data=data)
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
