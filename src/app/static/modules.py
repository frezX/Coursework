from typing import Optional
from jinja2 import Template
from src.consts import static
from aiohttp.web import Request


class Modules:
    def __init__(self):
        self.config: dict = static.CONFIG

    @staticmethod
    async def get_template(path: str) -> Template:
        with open(file=path) as source:
            return Template(source=source.read())

    async def get_data(self, request: Request, path: str) -> Optional[dict]:
        data: dict = self.config[path]['data']
        if data.get('token'):
            data['token']: str = request.headers.get('Referer').split('/')[-1]
        return data

    async def get_content_type(self, request: Request, path: str) -> str:
        if content_type := self.config[path].get('content_type'):
            return content_type
        return request.headers.get('Accept')
