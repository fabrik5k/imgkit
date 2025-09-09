from typing import Final, Literal

APP_NAME: Final[str] = 'pictokit'
PIXEL_MIN: Final[int] = 0
PIXEL_MAX: Final[int] = 255
RGB_CHANNELS: Final[int] = 3
RGB_DIM: Final[int] = 3
GREY_SCALE_DIM: Final[int] = 2
GREY_SCALE_CHANNEL_DIM: Final[int] = 1

# Types
Mode = Literal['gray', 'color', 'any']
