from src.logger import Logger
from aiohttp.web import Request
from json import JSONDecodeError
from typing import Optional, Any
from src.schemes import ColorRGB
from src.modules.colored import colored
from aiohttp.web_request import BaseRequest
from src.consts import colors, log_levels, exceptions, log_const

logger: Logger = Logger()


def status(name: str) -> callable:
    name: str = f'<{name}>'

    def wrapper(func: callable) -> callable:
        def inner(*args, **kwargs) -> Any:
            colored_name: str = colored(text=f'{name:{log_const.MAX_NAME_LEN}}')
            try:
                logger.info(text=f'{colored_name} Start')
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                ...
            except Exception as exc:
                logger.error(text=f'{colored_name} Error: {exc}')
                logger.exception(exc=exc)
            finally:
                logger.info(text=f'{colored_name} Stop')

        return inner

    return wrapper


def app_logger(level: log_levels = log_levels.INFO, name: Optional[str] = None) -> callable:
    def wrapper(func: callable) -> callable:
        name_: str = f'<{name or func.__name__}>'

        async def get_based_text(request: BaseRequest) -> str:
            try:
                json: dict = await request.json()
            except JSONDecodeError:
                json: dict = {}
            return f'{colored(text="Method", color=colors.PURPLE)}: {request.method:{log_const.MAX_METHOD_LEN}}' \
                   f'  {colored("|")}  ' \
                   f'{colored(text="From", color=colors.PURPLE)}: {request.remote:{log_const.MAX_FROM_LEN}}' \
                   f'  {colored("|")}  ' \
                   f'{colored(text="Path", color=colors.PURPLE)}: {request.path:{log_const.MAX_PATH_LEN}}' \
                   f'  {colored("|")}  ' \
                   f'{colored(text="Params", color=colors.PURPLE)}: {dict(request.rel_url.query)}' \
                   f'  {colored("|")}  ' \
                   f'{colored(text="Data", color=colors.PURPLE)}: {json}'

        async def log(
                request: BaseRequest, color: ColorRGB = colors.GREEN, log_level: log_levels = log_levels.INFO
        ) -> None:
            logger.log(
                text=f'{colored(text=f"{name_:{log_const.MAX_NAME_LEN}}", color=color)} '
                     f'{await get_based_text(request=request)}',
                level=log_level
            )

        async def inner(request: BaseRequest) -> Any:
            try:
                responce: Any = await func(request=request)
            except exceptions.AppExceptions as e:
                if type(e) in (exceptions.NotFound, exceptions.MethodNotAllowed):
                    color: ColorRGB = colors.YELLOW
                    log_level = log_levels.WARNING
                else:
                    color: ColorRGB = colors.RED
                    log_level = log_levels.ERROR
                await log(request=request, color=color, log_level=log_level)
                return exceptions.app_exception_handler(exception=type(e))
            # except exceptions.ApiExceptions as e:
            #     logger.error(
            #         text=f'{colored(text=f"{name_:{log_const.MAX_NAME_LEN}}", color=colors.YELLOW)} '
            #              f'{await get_based_text(request=request)}  {colored("|")}  '
            #              f'{colored(text="Exception:", color=colors.YELLOW)} '
            #              f'{colored(text=e.description)}'
            #     )
            #     return exceptions.api_exception_handler(exception=type(e))
            except Exception as exc:
                logger.error(
                    text=f'{colored(text=f"{name_:{log_const.MAX_NAME_LEN}}", color=colors.RED)} '
                         f'{await get_based_text(request=request)}  {colored("|")}  '
                         f'{colored(text="Error:", color=colors.RED)} '
                         f'{colored(text=exc.__str__())}'
                )
                logger.exception(exc=exc)
                return exceptions.app_exception_handler(exception=exceptions.InternalServerError)
            if level == log_levels.DEBUG:
                await log(request=request, log_level=level)
            else:
                await log(request=request)
            return responce

        return inner

    return wrapper


def websocketslogger(func: callable) -> callable:
    name: str = '<WS_Handler>'
    colored_name: str = colored(text=f'{name:{log_const.MAX_NAME_LEN}}', color=colors.ORANGE)

    async def log(text: str, path: str) -> None:
        logger.info(text=f'{colored_name} {text:40}|  {colored(text="Path", color=colors.PURPLE)}: /{path}')

    async def new_connection(path: str) -> None:
        await log(text='New connection!', path=path)

    async def wrapper(request: Request) -> Any:
        path: str = request.match_info.get('path')
        try:
            await new_connection(path=path)
            responce: Any = await func(request=request, path=path)
        except exceptions.AppExceptions as exc:
            await log(text=f'Error | match_info: {request.match_info}', path=path)
            return exceptions.app_exception_handler(exception=type(exc))
        except Exception as exc:
            return logger.exception(exc=exc)
        await log(text='Close connection!', path=path)
        return responce

    return wrapper
