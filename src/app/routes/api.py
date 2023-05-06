from src.consts import log_levels
from aiohttp.web import Request, Response
from src.app.api.handler import ApiHandler
from src.modules.decorators import app_logger
from src.consts.exceptions import MethodNotAllowed

handler: ApiHandler = ApiHandler()


@app_logger(level=log_levels.DEBUG, name='ApiHandler')
async def api_handler(request: Request) -> Response:
    if request.method != 'POST':
        raise MethodNotAllowed
    path: str = request.match_info.get('path')
    data: dict = dict(await request.post())
    return await handler(request=request, path=path, data=data)
