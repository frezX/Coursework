from enum import Enum
from time import strftime


class Formats(str, Enum):
    TIME_FORMAT: str = "%d.%m.%y|%X"


class TimeFormatter:
    def __init__(self, time_format: str = Formats.TIME_FORMAT):
        self._time_format: str = time_format

    @property
    def str_time(self) -> str:
        return strftime(self._time_format)
