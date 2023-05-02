from glob import glob
from src.app.static import StaticHandler
from src.modules.decorators import app_logger
from src.consts import log_levels, exceptions, static
from aiohttp.web import Request, Response, FileResponse

handler: StaticHandler = StaticHandler()


def static_handler(prefix: str):
    @app_logger(level=log_levels.DEBUG, name='StaticHandler')
    async def wrapper(request: Request) -> Response | FileResponse:
        path: str = request.match_info.get("path")
        full_path: str = f'web/static/{prefix}/{path}'
        if full_path in static.CONFIG:
            return await handler(request=request, path=full_path)
        if full_path in glob(pathname=f'web/static/{prefix}/**', recursive=True):
            return FileResponse(path=full_path)
        raise exceptions.NotFound

    return wrapper
