from typing import NoReturn
from aiohttp.web import Request, Response
from src.consts import log_levels, exceptions
from src.modules.decorators import app_logger


@app_logger(level=log_levels.DEBUG, name='WsHandler')
async def ws_handler(request: Request) -> Response | NoReturn:
    raise exceptions.NotFound(request)
