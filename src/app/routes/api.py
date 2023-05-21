from typing import NoReturn
from src.logger import Logger
from src.consts import log_levels
from src.consts.web import WebConsts
from src.app.api.handler import ApiHandler
from src.modules.web import validate_cookies
from src.modules.decorators import app_logger
from src.modules.tools import decode_form_data
from src.db.interaction import UserInteraction
from src.consts.routes import WebRoutes, ApiRoutes
from aiohttp.web import Request, Response, HTTPFound
from src.consts.exceptions import MethodNotAllowed, InternalServerError

logger: Logger = Logger()
handler: ApiHandler = ApiHandler()
user_interaction: UserInteraction = UserInteraction()


@app_logger(level=log_levels.DEBUG, name='ApiHandler')
async def api_handler(request: Request) -> Response | HTTPFound | NoReturn:
    if (path := request.match_info.get('path')) not in (ApiRoutes.LOGIN, ApiRoutes.CREATE_USER):
        cookies: dict = dict(request.cookies)
        if not cookies or not await validate_cookies(cookies=cookies, needed_cookies=WebConsts.NEEDED_COOKIES)\
                or not await user_interaction.verify_user_with_cookies(cookies=cookies):
            return HTTPFound(location=f'/{WebRoutes.LOGIN}')
    if path not in (ApiRoutes.TAKE_BOOK, ApiRoutes.RETURN_BOOK, ApiRoutes.STATISTICS_BOOK) and request.method != 'POST':
        raise MethodNotAllowed
    try:
        data: dict = await decode_form_data(request=request)
    except Exception as exc:
        logger.exception(exc=exc)
        raise InternalServerError
    return await handler(request=request, path=path, data=data)
