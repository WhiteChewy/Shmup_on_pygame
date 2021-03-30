from enum import Enum

from pygame import font

FONT_NAME = font.match_font('arial')

WIDTH = 480  # Ширина игрового окна
HEIGHT = 600  # высота игровго окна
FPS = 60  # частота кадров в секунду


class COLOR(Enum):
    # RGB ЦВЕТА
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
