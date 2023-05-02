from pydantic import BaseModel, Field


class ColorRGB(BaseModel):
    r: int = Field(default=0, ge=0, le=255)
    g: int = Field(default=0, ge=0, le=255)
    b: int = Field(default=0, ge=0, le=255)

    @property
    def tuple(self) -> tuple:
        return self.r, self.g, self.b

    def __iter__(self):
        for color_channel in self.tuple:
            yield color_channel
