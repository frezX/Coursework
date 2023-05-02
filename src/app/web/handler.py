from src.consts import templates
from aiohttp.web import Response, Request
from src.consts.exceptions import NotFound
from src.modules.web import render_template


class WebHandler:
    @staticmethod
    async def index(path: str, data: dict) -> tuple[str, dict]:
        print(data)
        params: dict = {
            'data': data
        }
        return templates[path], params

    @staticmethod
    async def login(path: str, data: dict) -> tuple[str, dict]:
        print(data)
        params: dict = {
            'data': data
        }
        return templates[path], params

    @staticmethod
    async def registration(path: str, data: dict) -> tuple[str, dict]:
        print(data)
        params: dict = {
            'data': data
        }
        return templates[path], params

    async def handler(self, path: str, data: dict) -> tuple[str, dict]:
        match path:
            case '':
                template, params = await self.index(path='index', data=data)
            case 'login':
                template, params = await self.login(path=path, data=data)
            case 'registration':
                template, params = await self.registration(path=path, data=data)
            case _:
                raise NotFound
        return template, params

    async def __call__(self, request: Request, path: str, data: dict) -> Response:
        template, params = await self.handler(path=path, data=data)
        return await render_template(request=request, template=template, params=params)
