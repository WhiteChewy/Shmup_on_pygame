# Скеллет игрового цикла в Pygame
import pygame
import random
from os import path
from constants import *
from player import Player
from bullet import Bullet
from mob import Mob


# выстрел объекта
def shoot(hero):
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


def mob_ini(n):
    for i in range(8):
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)


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
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    mob_ini(8)

    score = 0

    pygame.mixer.music.play(loops=-1)
    # игровой цикл
    running = True
    while running:
        CLOCK.tick(FPS)  # держим цикл на правильной скорости.
        # Обработка событий
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(player)

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
        SCREEN.fill(COLOR.BLACK.value)  # заливка окна черным
        SCREEN.blit(new_background, BACKGROUND_RECT)
        all_sprites.draw(SCREEN)
        draw_text(SCREEN, "YOUR SCORE: " + str(score), 18, WIDTH / 2, 10)
        pygame.display.flip()  # отображение отрифф сованного экрана

    pygame.quit()
