from enum import Enum
import pygame
from os import path


class COLOR(Enum):
    # RGB ЦВЕТА
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


FONT_NAME = pygame.font.match_font('arial')
WIDTH = 480  # Ширина игрового окна
HEIGHT = 600  # высота игровго окна
FPS = 60  # частота кадров в секунду
METEOR_LIST = ['meteorBig.png', 'meteorSmall.png']
SOUNDS = ['exp1.wav', 'exp2.wav']
ASSETS = path.join(path.dirname(__file__), "assets")
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # создание окна игры
CLOCK = pygame.time.Clock()
BACKGROUND = pygame.image.load(path.join(ASSETS, "starBackground.png")).convert()
BACKGROUND_RECT = BACKGROUND.get_rect()
PLAYER_ASSET = pygame.image.load(path.join(ASSETS, 'sampleShip3.png')).convert()
LIVES = pygame.transform.scale(PLAYER_ASSET, (35, 20))
LIVES.set_colorkey(COLOR.BLACK.value)
METEOR_ASSET = pygame.image.load(path.join(ASSETS, 'meteorBig.png')).convert()
BULLET_ASSET = pygame.image.load(path.join(ASSETS, 'laserGreen.png')).convert()
SOUND_DIR = path.join(path.dirname(__file__), "sound")
METEOR_IMAGES = []
for img in METEOR_LIST:
    METEOR_IMAGES.append(pygame.image.load(path.join(ASSETS, img)).convert())
HEALTHBAR_LENGTH = 100
HEALTHBAR_HEIGHT = 10
