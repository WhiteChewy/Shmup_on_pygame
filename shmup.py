# Скеллет игрового цикла в Pygame
import pygame
import random

# блок определения размеров окна и фпс
WIDTH = 480  # Ширина игрового окна
HEIGHT = 600  # высота игровго окна
FPS = 60  # частота кадров в секунду

# RGB ЦВЕТА
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# далее инициализируется игра и окно
pygame.init()   # "запуск pygame"
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание окна игры
pygame.display.set_caption("Shoot 'em UP!")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))  # размер спрайта игрока
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0  # скорость с которй движется игрок по оси х
        self.speedy = 0  # скорость с которой движется игрок по оси y

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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, 40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)
# игровой цикл
running = True
while running:
    clock.tick(FPS)  # держим цикл на правильной скорости.
    # Обработка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()

    # проверка столкновений
    bullet_hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in bullet_hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    # Рендеринг
    screen.fill(BLACK)  # заливка окна черным
    all_sprites.draw(screen)
    pygame.display.flip()  # отображение отрисованного экрана

pygame.quit()
