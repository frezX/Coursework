from aiohttp.web import Request, Response, HTTPFound
from aiohttp_jinja2 import render_template as jinja_render_template


async def render_template(request: Request, template: str, params: dict, status: int = 200) -> Response:
    return jinja_render_template(template_name=template, request=request, context=params, status=status)


async def set_cookies(redirect: HTTPFound, cookies: dict) -> None:
    for name, value in cookies.items():
        redirect.set_cookie(name=name, value=value)


async def validate_cookies(cookies: dict, needed_cookies: tuple[str, ...]) -> bool:
    return all(cookie in needed_cookies for cookie in cookies)

