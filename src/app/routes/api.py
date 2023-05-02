from aiohttp.web import Request, Response
from src.consts import log_levels, exceptions
from src.modules.decorators import app_logger


@app_logger(level=log_levels.DEBUG, name='ApiHandler')
async def api_handler(request: Request) -> Response:
    raise exceptions.NotFound(request)
