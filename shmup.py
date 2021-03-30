import random
from os import path

import pygame

from constants import FONT_NAME, WIDTH, HEIGHT, FPS, COLOR


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_asset, (70, 40))
        self.image.set_colorkey(COLOR.BLACK.value)
        self.rect = self.image.get_rect()
        self.radius = 31
        #  pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
        shoot_sound.play()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(meteor_images)
        self.image_original.set_colorkey(COLOR.BLACK.value)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, 40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-4, 4)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_original, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_asset
        self.image.set_colorkey(COLOR.BLACK.value)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, COLOR.WHITE.value)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


if __name__ == '__main__':
    # далее инициализируется игра и окно
    pygame.init()  # "запуск pygame"
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание окна игры
    pygame.display.set_caption("Shoot 'em UP!")
    clock = pygame.time.Clock()

    # загрузка графики
    assets = path.join(path.dirname(__file__), "assets")
    background = pygame.image.load(path.join(assets, "starBackground.png")).convert()
    background_rect = background.get_rect()
    # растягиваем фон на все окно
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    player_asset = pygame.image.load(path.join(assets, 'sampleShip3.png')).convert()
    meteor_asset = pygame.image.load(path.join(assets, 'meteorBig.png')).convert()
    bullet_asset = pygame.image.load(path.join(assets, 'laserGreen.png')).convert()

    # звук
    sound_dir = path.join(path.dirname(__file__), "sound")
    shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "shoot.wav"))
    exp_sounds = []
    for sound in ['exp1.wav', 'exp2.wav']:
        exp_sounds.append(pygame.mixer.Sound(path.join(sound_dir, sound)))

    pygame.mixer.music.load(path.join(sound_dir, "DEmo_3.ogg"))
    pygame.mixer.music.set_volume(0.5)
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    meteor_images = []
    meteor_list = ['meteorBig.png', 'meteorSmall.png']
    for img in meteor_list:
        meteor_images.append(pygame.image.load(path.join(assets, img)).convert())

    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)

    score = 0
    pygame.mixer.music.play(loops=-1)

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
            score += 60 - hit.radius
            random.choice(exp_sounds).play()
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            running = False
        # Рендеринг
        screen.fill(COLOR.BLACK.value)  # заливка окна черным
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, "YOUR SCORE: " + str(score), 18, WIDTH / 2, 10)
        pygame.display.flip()  # отображение отрифф сованного экрана

    pygame.quit()
