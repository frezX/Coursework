from json import JSONDecodeError
from src.consts import log_levels
from aiohttp.web import Request, Response
from src.app.web.handler import WebHandler
from src.consts.exceptions import NotFound
from src.modules.decorators import app_logger

handler: WebHandler = WebHandler()


@app_logger(level=log_levels.DEBUG, name='WebHandler')
async def web_handler(request: Request) -> Response:
    path: str = request.match_info.get('path')
    data: dict = {}
    match request.method:
        case 'GET':
            try:
                data['get'] = await request.json()
            except JSONDecodeError:
                ...
        case 'POST':
            data['post'] = dict(await request.post())
        case _:
            raise NotFound
    if params := request.rel_url.query:
        data['params'] = dict(params)
    return await handler(request=request, path=path, data=data)
