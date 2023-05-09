from os import system
from typing import NoReturn
from src.env import app_env
from src.logger import Logger
from src.modules.decorators import status
from src.application import app, event_loop
from aiohttp.web import Application, run_app

logger: Logger = Logger(name='Main')


class Main:
    def __init__(self):
        self.app: Application = app

    @status(name='Application')
    def run_app(self) -> NoReturn:
        run_app(
            app=self.app,
            loop=event_loop,
            host=app_env.host,
            port=app_env.port,
            print=lambda *args, **kwargs: ...
        )

    def run(self) -> NoReturn:
        self.run_app()


if __name__ == '__main__':
    system("clear")
    system("stty -echo")
    try:
        main: Main = Main()
        main.run()
    except BaseException as exc:
        logger.exception(exc=exc)
    finally:
        system("stty echo")
