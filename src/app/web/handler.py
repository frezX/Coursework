from src.consts import templates
from src.consts.routes import WebRoutes
from src.consts.exceptions import NotFound
from aiohttp.web import Response, Request, HTTPFound
from src.modules.web import render_template, validate_cookies


class WebHandler:
    def __init__(self):
        self.needed_cookies: tuple[str, ...] = ('id', 'role', 'login', 'session')

    async def index(self, request: Request) -> tuple[str, dict]:
        cookies: dict = dict(request.cookies)
        if not cookies or not await validate_cookies(cookies=cookies, needed_cookies=self.needed_cookies):
            raise HTTPFound(location=f'/{WebRoutes.LOGIN}')
        user_id: int = cookies['id']
        role: str = cookies['role']
        login: str = cookies['login']
        session: str = cookies['session']
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

    async def handler(self, request: Request, path: str, data: dict) -> tuple[str, dict]:
        match path:
            case WebRoutes.INDEX:
                template, params = await self.index(request=request)
            case WebRoutes.LOGIN | WebRoutes.REGISTRATION:
                template, params = await self.default_route_handler(path=path, data=data)
            case _:
                raise NotFound
        return template, params

    async def __call__(self, request: Request, path: str, data: dict) -> Response:
        try:
            template, params = await self.handler(request=request, path=path, data=data)
            return await render_template(request=request, template=template, params=params)
        except HTTPFound as redirect:
            return redirect
