from aiohttp.web import Request, Response
from aiohttp_jinja2 import render_template as jinja_render_template


async def render_template(request: Request, template: str, params: dict, status: int = 200) -> Response:
    return jinja_render_template(template_name=template, request=request, context=params, status=status)
