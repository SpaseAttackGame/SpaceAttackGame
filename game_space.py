import pygame
import control
import time
from stats import Stats
from scores import Scores
from gun import Gun
from pygame.sprite import Group
from button import Button
from bunker import create_bunkers
import random
import sys


# Выносим отрисовку звездного неба в отдельную чистую функцию
def draw_stars(screen, stars, bg_color):
    screen.fill(bg_color)
    for star in stars:
        star['y'] += star['speed']
        if star['y'] > 600:
            star['y'] = 0
            star['x'] = random.randint(0, 600)
        pygame.draw.circle(screen, (200, 200, 255), (int(star['x']), int(star['y'])), 1)

import math
# === СВЕРХНАДЁЖНАЯ ФУНКЦИЯ ГЛАВНОГО МЕНЮ ===
def draw_main_menu(screen, font_title, font_bold, mouse_pos, click_fired, stats, sc, inos, bullets, ufo_group,
                   particles):
    # === 🚀 ПРОКАЧАННЫЙ НЕОНОВЫЙ 3D ЗАГОЛОВОК С ЭФФЕКТОМ НЕВЕСОМОСТИ ===
    text_string = "SPACE ATTACK"

    # Считаем смещение по вертикали с помощью синуса от текущего времени
    # time.time() * 3 задает скорость покачивания, а число 8 — высоту волны (в пикселях)
    wave_offset = math.sin(time.time() * 3) * 8

    # Базовая позиция по Y теперь динамическая (60 + покачивание)
    title_x = 300 - font_title.size(text_string)[0] // 2
    title_y = 60 + wave_offset

    # 1. Рисуем глубокую фиолетовую размытую тень (сдвигаем во все стороны на 3 пикселя)
    shadow_color = (150, 0, 255)
    shadow_surf = font_title.render(text_string, True, shadow_color)

    screen.blit(shadow_surf, (title_x - 3, title_y - 3))
    screen.blit(shadow_surf, (title_x + 3, title_y - 3))
    screen.blit(shadow_surf, (title_x - 3, title_y + 3))
    screen.blit(shadow_surf, (title_x + 3, title_y + 3))

    # 2. Рисуем мягкое голубое свечение чуть ближе (на 1 пиксель)
    glow_color = (0, 150, 255)
    glow_surf = font_title.render(text_string, True, glow_color)
    screen.blit(glow_surf, (title_x - 1, title_y - 1))
    screen.blit(glow_surf, (title_x + 1, title_y - 1))
    screen.blit(glow_surf, (title_x - 1, title_y + 1))
    screen.blit(glow_surf, (title_x + 1, title_y + 1))

    # 3. Накладываем сверху основной ярко-бирюзовый текст киберпанка
    main_surf = font_title.render(text_string, True, (0, 255, 255))
    screen.blit(main_surf, (title_x, title_y))

    # Прямоугольники кнопок меню по центру (X = 200) остаются без изменений
    rect_play = pygame.Rect(200, 180, 200, 45)
    rect_settings = pygame.Rect(200, 245, 200, 45)
    rect_controls = pygame.Rect(200, 310, 200, 45)
    rect_shop = pygame.Rect(200, 375, 200, 45)
    rect_exit = pygame.Rect(200, 440, 200, 45)

    color_play = (0, 255, 150) if rect_play.collidepoint(mouse_pos) else (0, 180, 100)
    color_settings = (255, 200, 0) if rect_settings.collidepoint(mouse_pos) else (180, 140, 0)
    color_controls = (0, 150, 255) if rect_controls.collidepoint(mouse_pos) else (0, 100, 200)
    color_shop = (0, 255, 255) if rect_shop.collidepoint(mouse_pos) else (0, 180, 180)
    color_exit = (255, 50, 50) if rect_exit.collidepoint(mouse_pos) else (180, 40, 40)

    clean_buttons = [
        (rect_play, "Играть", color_play),
        (rect_settings, "Настройки", color_settings),
        (rect_controls, "Управление", color_controls),
        (rect_shop, "Магазин (M)", color_shop),
        (rect_exit, "Выход", color_exit)
    ]

    for r, text, col in clean_buttons:
        pygame.draw.rect(screen, col, r)
        pygame.draw.rect(screen, (255, 255, 255), r, 1)
        txt_s = font_bold.render(text, True, (255, 255, 255))
        screen.blit(txt_s, (r.centerx - txt_s.get_width() // 2, r.centery - txt_s.get_height() // 2))

    if click_fired:
        if rect_play.collidepoint(mouse_pos):
            stats.reset_stats()
            if hasattr(sc, 'prep_score'):
                sc.prep_score()
                sc.prep_level()
                sc.prep_guns()
            elif hasattr(sc, 'image_score'):
                sc.image_score()

            inos.empty()
            bullets.empty()
            ufo_group.empty()
            particles.empty()
            import control
            control.create_army(screen, inos, stats)

            stats.run_game = True
            stats.ufo_active = False
            stats.ufo_last_spawn = time.time()
            stats.current_weapon = "plasma"
            stats.plasma_mode = "ready"
            stats.game_paused = False
            print("🚀 Боевой режим успешно запущен!")
            return "GAME_ACTIVE"

        elif rect_settings.collidepoint(mouse_pos):
            return "SETTINGS"

        elif rect_controls.collidepoint(mouse_pos):
            return "CONTROLS"

        elif rect_shop.collidepoint(mouse_pos):
            from shop import show_shop
            show_shop(screen, stats, sc)
            return "MENU"

        elif rect_exit.collidepoint(mouse_pos):
            sys.exit()

    return "MENU"

def draw_settings(screen, font_title, font_bold, mouse_pos, click_fired, hit_sound, stats):
    global alien_speed_multiplier, sound_enabled

    set_title = font_title.render("НАСТРОЙКИ", True, (255, 200, 0))
    screen.blit(set_title, (300 - set_title.get_width() // 2, 80))

    # Рассчитываем динамические тексты
    msg_speed = f"Скорость: x{alien_speed_multiplier:.1f}"
    msg_sound = "Звук: ВКЛ" if sound_enabled else "Звук: ВЫКЛ"

    # Прямоугольники кнопок НАСТРОЕК (Справа, X = 320)
    rect_speed = pygame.Rect(320, 220, 200, 45)
    rect_sound = pygame.Rect(320, 285, 200, 45)
    rect_back = pygame.Rect(320, 350, 200, 45)

    color_speed = (0, 255, 255) if rect_speed.collidepoint(mouse_pos) else (0, 150, 150)
    color_sound = (0, 255, 255) if rect_sound.collidepoint(mouse_pos) else (0, 150, 150)
    color_back = (255, 50, 50) if rect_back.collidepoint(mouse_pos) else (150, 50, 50)

    settings_buttons = [
        (rect_speed, msg_speed, color_speed),
        (rect_sound, msg_sound, color_sound),
        (rect_back, "Назад", color_back)
    ]

    for r, text, col in settings_buttons:
        pygame.draw.rect(screen, col, r)
        pygame.draw.rect(screen, (255, 255, 255), r, 1)
        txt_s = font_bold.render(text, True, (255, 255, 255))
        screen.blit(txt_s, (r.centerx - txt_s.get_width() // 2, r.centery - txt_s.get_height() // 2))

    if click_fired:
        if rect_speed.collidepoint(mouse_pos):
            alien_speed_multiplier = 1.5 if alien_speed_multiplier == 1.0 else (
                2.0 if alien_speed_multiplier == 1.5 else 1.0)
            return "SETTINGS"
        elif rect_sound.collidepoint(mouse_pos):
            sound_enabled = not sound_enabled
            hit_sound.set_volume(0.4 if sound_enabled else 0.0)
            return "SETTINGS"
        elif rect_back.collidepoint(mouse_pos):
            return "MENU"

    return "SETTINGS"


def run():
    global alien_speed_multiplier, sound_enabled
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("SPACE ATTACK")
    bg_color = (0, 0, 0)

    hit_sound = pygame.mixer.Sound("hit.mp3")
    hit_sound.set_volume(0.4)

    stats = Stats()
    sc = Scores(screen, stats)
    gun = Gun(screen, stats)

    inos = Group()
    bullets = Group()
    bunkers = Group()
    ufo_group = Group()
    particles = Group()

    stars = []
    for _ in range(40):
        stars.append({
            'x': random.randint(0, 600),
            'y': random.randint(0, 600),
            'speed': random.uniform(1.0, 3.5)
        })
    clock = pygame.time.Clock()

    base_alien_speed = 0.3
    alien_speed_multiplier = 1.0
    sound_enabled = True

    control.create_army(screen, inos, stats)
    create_bunkers(screen, bunkers)

    font_title = pygame.font.SysFont("Arial", 48)
    font_desc = pygame.font.SysFont("Arial", 20)
    font_bold = pygame.font.SysFont("Arial", 26, bold=True)

    start_game_button = Button(screen, "Я понял", y_offset=150)

    stats.ufo_last_spawn = time.time()
    stats.ufo_spawn_delay = 15.0
    stats.ufo_active = False
    stats.run_game = False

    game_state = "MENU"
    start_time_disclaimer = time.time()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        click_fired = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Пересылаем одиночные нажатия клавиш в control только во время активного боя
            if game_state == "GAME_ACTIVE":
                control.events(event, screen, gun, bullets, stats, inos, particles, sc)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_fired = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and game_state == "MENU":
                    from shop import show_shop
                    show_shop(screen, stats, sc)

        alien_speed = base_alien_speed * alien_speed_multiplier

        # Рисуем звёздное небо всегда, когда не идёт активный бой
        if game_state != "GAME_ACTIVE":
            draw_stars(screen, stars, bg_color)

        # === 🛸 ПЕРЕКЛЮЧАТЕЛЬ ЭКРАНОВ БЕЗ НАЛОЖЕНИЙ ===
        if game_state == "MENU":
            # Рисуем ТОЛЬКО центрированное главное меню
            game_state = draw_main_menu(screen, font_title, font_bold, mouse_pos, click_fired, stats, sc, inos, bullets,
                                        ufo_group, particles)

        elif game_state == "SETTINGS":
            game_state = draw_settings(screen, font_title, font_bold, mouse_pos, click_fired, hit_sound, stats)

        elif game_state == "CONTROLS":
            # Загружаем экран управления из отдельного файла
            import controls_menu
            game_state = controls_menu.draw_controls_screen(screen, font_title, font_bold, font_desc, mouse_pos,
                                                            click_fired)

        elif game_state == "GAME_ACTIVE":
            if not getattr(stats, 'game_paused', False):
                pygame.mouse.set_visible(False)
                gun.update_gun()

                if not stats.ufo_active and (time.time() - stats.ufo_last_spawn > stats.ufo_spawn_delay):
                    from ufo import Ufo
                    stats.ufo_max_hp = 10
                    boss = Ufo(screen, stats)
                    ufo_group.add(boss)
                    stats.ufo_hp = stats.ufo_max_hp
                    stats.ufo_active = True
                    print("🛸 Прилетел Босс!")

                particles.update()

                alien_speed = control.update_bullets(screen, stats, sc, inos, bullets, alien_speed, particles,
                                                     ufo_group, hit_sound)
                control.update_inos(stats, screen, sc, gun, inos, bullets, alien_speed, particles, ufo_group, bunkers)
                control.update(bg_color, screen, stats, sc, gun, inos, bullets, particles, bunkers, ufo_group)

            else:
                # Меню паузы
                pygame.mouse.set_visible(True)
                from pause import show_pause
                pause_choice = show_pause(screen, stats)
                if pause_choice == "TO_MENU":
                    game_state = "MENU"

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run()
