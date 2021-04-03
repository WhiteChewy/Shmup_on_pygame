# Скеллет игрового цикла в Pygame
import pygame
import random
from os import path
from constants import *
from player import Player
from bullet import Bullet
from mob import Mob


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, explosion_animation):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# выстрел объекта
def shoot(hero):
    now = pygame.time.get_ticks()
    if now - hero.last_shot > hero.shoot_delay:
        hero.last_shot = now
        bullet = Bullet(hero.rect.centerx, hero.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


#  рендер текста
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, COLOR.WHITE.value)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# отрисовка астеройдов
def mob_ini(n):
    for i in range(n):
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)


# отрисовка индикатора жизни
def draw_healthbar(surface, x, y, filled):
    if filled < 0:
        filled = 0
    fill = (filled / 100) * HEALTHBAR_LENGTH
    outline_rect = pygame.Rect(x, y, HEALTHBAR_LENGTH, HEALTHBAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, HEALTHBAR_HEIGHT)
    pygame.draw.rect(surface, COLOR.GREEN.value, fill_rect)
    pygame.draw.rect(surface, COLOR.WHITE.value, outline_rect, 2)


def explosion_init():
    explosion = {'large': [], 'small': [], 'player': []}
    for i in range(9):
        file = 'regularExplosion0{}.png'.format(i)
        image = pygame.image.load(path.join(ASSETS, file)).convert()
        image.set_colorkey(COLOR.BLACK.value)
        img_lg = pygame.transform.scale(image, (75, 75))
        explosion['large'].append(img_lg)
        img_sm = pygame.transform.scale(image, (32, 32))
        explosion['small'].append(img_sm)
        file = 'sonicExplosion0{}.png'.format(i)
        image = pygame.image.load(path.join(ASSETS, file)).convert()
        image.set_colorkey(COLOR.BLACK.value)
        explosion['player']. append(image)
    return explosion


# отрисовка количества жизней
def draw_lives(surface, x, y, lives, image):
    for i in range(lives):
        image_rect = image.get_rect()
        image_rect.x = x + 40 * i
        image_rect.y = y
        surface.blit(image, image_rect)


def show_gameover_screen():
    SCREEN.blit(new_background, BACKGROUND_RECT)
    draw_text(SCREEN, "Shoot 'em UP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(SCREEN, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(SCREEN, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


if __name__ == "__main__":
    # далее инициализируется игра и окно
    pygame.init()   # "запуск pygame"
    pygame.mixer.init()
    pygame.display.set_caption("Shoot 'em UP!")

    # растягиваем фон на все окно
    new_background = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

    # звук
    shoot_sound = pygame.mixer.Sound(path.join(SOUND_DIR, "shoot.wav"))
    exp_sounds = []
    for sound in SOUNDS:
        exp_sounds.append(pygame.mixer.Sound(path.join(SOUND_DIR, sound)))
    pygame.mixer.music.load(path.join(SOUND_DIR, "DEmo_3.ogg"))
    pygame.mixer.music.set_volume(0.5)

    # инициализация спрайтов
    all_sprites = pygame.sprite.Group()
    explosion_sprite = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    explosion = explosion_init()
    mob_ini(8)

    score = 0

    pygame.mixer.music.play(loops=-1)
    # игровой цикл
    running = True
    game_over = True
    while running:
        if game_over:
            show_gameover_screen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            mob_ini(8)
            score = 0
        CLOCK.tick(FPS)  # держим цикл на правильной скорости.
        # Обработка событий
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(player)

        # Обновление1
        all_sprites.update()

        # проверка столкновений
        bullet_hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in bullet_hits:
            score += 60 - hit.radius
            random.choice(exp_sounds).play()
            expl = Explosion(hit.rect.center, 'large', explosion)
            all_sprites.add(expl)
            mob_ini(1)

        # проверка столкновений игрока с мобом
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.health -= hit.radius * 0.5
            expl = Explosion(hit.rect.center, "small", explosion )
            all_sprites.add(expl)
            mob_ini(1)
            if player.health <= 0:
                death = Explosion(player.rect.center, 'player', explosion)
                all_sprites.add(death)
                player.hide()
                player.lives -= 1
                player.health = 100

        if player.lives == 0 and not death.alive():
            game_over = True


        # Рендеринг
        SCREEN.fill(COLOR.BLACK.value)  # заливка окна черным
        SCREEN.blit(new_background, BACKGROUND_RECT)
        all_sprites.draw(SCREEN)
        draw_text(SCREEN, "YOUR SCORE: " + str(score), 18, WIDTH / 2, 10)
        draw_healthbar(SCREEN, 5, 5, player.health)
        draw_lives(SCREEN, WIDTH - 115, 5, player.lives, LIVES)
        pygame.display.flip()  # отображение отрисованного экрана

    pygame.quit()
