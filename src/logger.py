from sys import stdout
from os import mkdir, path
from typing import Optional, NoReturn
from src.modules.colored import colored, clear_color
from traceback import TracebackException, FrameSummary
from src.modules.formatter import TimeFormatter, Formats
from src.consts import colors, log_levels, log_colors, log_const


class Logger:
    def __init__(self, name: Optional[str] = None, time_format: str = Formats.TIME_FORMAT):
        self.name: Optional[str] = f'<{name}>' if name else None
        self.time_formatter: TimeFormatter = TimeFormatter(time_format=time_format)

    @staticmethod
    def print(text: str) -> NoReturn:
        stdout.write(text)

    @staticmethod
    def save_in_log(text: str, level: log_levels) -> NoReturn:
        if not path.exists(path='log'):
            mkdir(path='log')
        with open(f'log/{level.name.lower()}.log', mode='a') as file:
            file.write(text)

    def log(self, text: str, level: log_levels = log_levels.INFO) -> NoReturn:
        time: str = f'[{self.time_formatter.str_time}]'
        colored_time: str = colored(text=time, color=colors.BLUE)
        if self.name:
            colored_name: str = colored(
                text=f'{self.name:{log_const.MAX_NAME_LEN}}',
                color=log_colors[level]
            )
            colored_text: str = f'{colored_time}: {colored_name} {text}\n'
        else:
            colored_text: str = f'{colored_time}: {text}\n'
        self.print(text=colored_text)
        if level in log_levels:
            self.save_in_log(text=clear_color(text=colored_text), level=level)

    def info(self, text: str) -> NoReturn:
        self.log(text=text)

    def debug(self, text: str) -> NoReturn:
        self.log(text=text, level=log_levels.DEBUG)

    def error(self, text: str) -> NoReturn:
        self.log(text=text, level=log_levels.ERROR)

    def warning(self, text: str) -> NoReturn:
        self.log(text=text, level=log_levels.WARNING)

    def critical(self, text: str) -> NoReturn:
        self.log(text=text, level=log_levels.CRITICAL)

    def exception(self, exc: BaseException) -> NoReturn:
        tb: FrameSummary = TracebackException.from_exception(exc).stack[-1]
        self.critical(
            text=f'{colored(text="Filename")}: {tb.filename.split("/")[-1]}   '
                 f'{colored(text="Function")}: {tb.name}   '
                 f'{colored(text="Line")}: {tb.lineno}   '
                 f'{colored(text="Codeline")}: {tb.line}   '
                 f'{colored(text="Error")}: {exc}   '
                 f'{colored(text="Full path")}: {tb.filename}'
        )
