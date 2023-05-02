from jinja2 import Template
from .modules import Modules
from aiohttp.web import Response, Request


class StaticHandler:
    def __init__(self):
        self.modules: Modules = Modules()

    async def handler(self, request: Request, path: str) -> Response:
        template: Template = await self.modules.get_template(path=path)
        data: dict = await self.modules.get_data(request=request, path=path)
        rendered_template: str = template.render(data)
        content_type: str = await self.modules.get_content_type(request=request, path=path)
        return Response(text=rendered_template, content_type=content_type)

    async def __call__(self, request: Request, path: str) -> Response:
        return await self.handler(request=request, path=path)
