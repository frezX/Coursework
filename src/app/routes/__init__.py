from src.env import app_env
from aiohttp.web import route
from src.app.routes.ws import ws_handler
from src.app.routes.api import api_handler
from src.app.routes.web import web_handler
from src.app.routes.static import static_handler

config_routes: dict = {
    'css': dict(
        path='/css/{path:.*}',
        method='*',
        handler=static_handler(prefix='css')
    ),
    'js': dict(
        path='/js/{path:.*}',
        method='*',
        handler=static_handler(prefix='js')
    ),
    'img': dict(
        path='/img/{path:.*}',
        method='*',
        handler=static_handler(prefix='img')
    ),
    'svg': dict(
        path='/svg/{path:.*}',
        method='*',
        handler=static_handler(prefix='svg')
    ),
    'ico': dict(
        path='/ico/{path:.*}',
        method='*',
        handler=static_handler(prefix='ico')
    ),
    'fonts': dict(
        path='/fonts/{path:.*}',
        method='*',
        handler=static_handler(prefix='fonts')
    ),
    'ws': dict(
        path='/ws/{path:.*}',
        method='*',
        handler=ws_handler
    ),
    'api': dict(
        path='/api/{path:.*}',
        method='*',
        handler=api_handler
    ),
    'web': dict(
        path='/{path:.*}',
        method='*',
        handler=web_handler
    )
}

ROUTES: list = [
    route(**config_routes.get(needed_route))
    for needed_route in config_routes
    if app_env.get(needed_route, True)
]
