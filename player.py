import pygame
from constants import PLAYER_ASSET, COLOR, WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(PLAYER_ASSET, (70, 40))
        self.image.set_colorkey(COLOR.BLACK.value)
        self.rect = self.image.get_rect()
        self.radius = 31
#        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0  # скорость с которй движется игрок по оси х
        self.speedy = 0  # скорость с которой движется игрок по оси y
        self.health = 100  # "здоровье" корабля
        self.shoot_delay = 250  # пауза между выстрелами в милдисекундах
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.speedy = 0
        # get_pressed() возвращает словарь со всеми клавишами и значениями Истина Ложь
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.speedx = -8
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.speedx = 8
        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            self.speedy = -8
        if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            self.speedy = 8
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy
