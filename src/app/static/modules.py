from aiofiles import open
from jinja2 import Template
from aiohttp.web import Request
from src.consts.static import CONFIG, ValueFromCookies, ValueFromHeaders


class Modules:
    def __init__(self):
        self.config: dict = CONFIG

    @staticmethod
    async def get_template(path: str) -> Template:
        async with open(file=path) as template:
            return Template(source=await template.read())

    async def get_data(self, request: Request, path: str) -> dict:
        data: dict = {}
        for param, value in self.config[path]['data'].items():
            if value is ValueFromCookies:
                data[param] = request.cookies.get(param, value)
            elif value is ValueFromHeaders:
                data[param] = request.headers.get(param, value)
            else:
                data[param] = value
        return data

    async def get_content_type(self, request: Request, path: str) -> str:
        if content_type := self.config[path].get('content_type'):
            return content_type
        return request.headers.get('Accept')
