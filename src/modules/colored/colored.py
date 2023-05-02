from re import compile
from typing import Union
from src.consts import colors
from src.schemes import ColorRGB

COLOR_PATTERN: str = r'\033\[(\d|;)+?m'


def colored(text: str, color: Union[ColorRGB, str] = colors.WHITE, bg: Union[ColorRGB, str] = None) -> str:
    if isinstance(color, str):
        color: ColorRGB = hex_to_rgb(hex_color=color)
    text: str = f'\033[38;2;{color.r};{color.g};{color.b}m' + text
    if bg:
        text: str = f'\033[48;2;{bg.r};{bg.g};{bg.b}m' + text
    return text + '\033[0m'


def hex_to_rgb(hex_color: str) -> ColorRGB:
    hex_color: str = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return ColorRGB(r=r, g=g, b=b)


def clear_color(text: str) -> str:
    return compile(COLOR_PATTERN).sub('', text)
