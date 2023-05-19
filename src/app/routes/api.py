from typing import NoReturn
from src.logger import Logger
from src.consts import log_levels
from aiohttp.web import Request, Response
from src.app.api.handler import ApiHandler
from src.modules.decorators import app_logger
from src.modules.tools import decode_form_data
from src.consts.exceptions import MethodNotAllowed, InternalServerError

logger: Logger = Logger()
handler: ApiHandler = ApiHandler()


@app_logger(level=log_levels.DEBUG, name='ApiHandler')
async def api_handler(request: Request) -> Response | NoReturn:
    if request.method != 'POST':
        raise MethodNotAllowed
    path: str = request.match_info.get('path')
    try:
        data: dict = await decode_form_data(request=request)
    except Exception as exc:
        logger.exception(exc=exc)
        raise InternalServerError
    return await handler(request=request, path=path, data=data)
