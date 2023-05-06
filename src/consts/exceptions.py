from aiohttp.web import Response


class Skip(BaseException):
    text: str = 'Skip'


class BadRequest(BaseException):
    status: int = 400
    text: str = f'{status} - Bad Request'


class Unauthorized(BaseException):
    status: int = 401
    text: str = f'{status} - Unauthorized'


class NotFound(BaseException):
    status: int = 404
    text: str = f'{status} - Not Found'


class MethodNotAllowed(BaseException):
    status: int = 405
    text: str = f'{status} - Method Not Allowed'


class InternalServerError(BaseException):
    status: int = 500
    text: str = f'{status} - Internal Server Error'


class DataError(BadRequest):
    text: str = f'{BadRequest.text}(Data Error)'


AppExceptions: tuple = (
    Skip,
    BadRequest,
    Unauthorized,
    NotFound,
    MethodNotAllowed,
    InternalServerError,
)


def app_exception_handler(exception: AppExceptions) -> Response:
    return Response(text=exception.text, status=exception.status)
