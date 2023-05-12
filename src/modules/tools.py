from time import time
from datetime import datetime


def get_timestamp() -> float:
    return time()


def strftime(timestamp: float = get_timestamp(), time_format: str = '%m.%d.%Y %H:%M:%S') -> str:
    return datetime.fromtimestamp(timestamp).strftime(time_format)
