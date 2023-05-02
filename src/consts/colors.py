from src.schemes import ColorRGB


class Colors:
    DARK = ColorRGB()
    WHITE = ColorRGB(r=255, g=255, b=255)
    RED = ColorRGB(r=255, g=40, b=40)
    GREEN = ColorRGB(r=40, g=255, b=40)
    BLUE = ColorRGB(r=40, g=40, b=255)
    ORANGE = ColorRGB(r=255, g=100)
    PURPLE = ColorRGB(r=255, g=10, b=255)
    YELLOW = ColorRGB(r=230, g=200)


class LogColors:
    DEBUG: ColorRGB = Colors.BLUE
    INFO: ColorRGB = Colors.GREEN
    WARNING: ColorRGB = Colors.YELLOW
    ERROR: ColorRGB = Colors.RED
    CRITICAL: ColorRGB = Colors.PURPLE

    def __getitem__(self, level: int) -> ColorRGB:
        match level:
            case 0:
                return self.DEBUG
            case 1:
                return self.INFO
            case 2:
                return self.WARNING
            case 3:
                return self.ERROR
            case 4:
                return self.CRITICAL
