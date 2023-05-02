from aiohttp_jinja2 import setup
from src.app.routes import ROUTES
from aiohttp.web import Application
from jinja2 import FileSystemLoader
from asyncio import AbstractEventLoop, new_event_loop, set_event_loop

# Event Loop
event_loop: AbstractEventLoop = new_event_loop()
set_event_loop(loop=event_loop)

# Application
app: Application = Application(loop=event_loop)
app.add_routes(routes=ROUTES)

setup(app=app, loader=FileSystemLoader(searchpath='web/templates'))

__all__: list = ['app', 'event_loop']
