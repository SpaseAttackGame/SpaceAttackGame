import pygame
import sys


def draw_controls_screen(screen, font_title, font_bold, font_desc, mouse_pos, click_fired):
    """Отображает красивый и понятный экран управления арсеналом"""
    screen.fill((0, 0, 0))  # Чистый черный космос

    title_surf = font_title.render("УПРАВЛЕНИЕ БОЕМ", True, (0, 255, 255))
    screen.blit(title_surf, (300 - title_surf.get_width() // 2, 50))

    # Текст раскладки кнопок
    desc_lines = [
        "Перемещение пушки: Клавиши A / D или Стрелочки",
        "Обычная стрельба: Зажать ПРОБЕЛ",
        "--------------------------------------------------",
        "❄️ Клавиша F (А) — Бомба заморозки времени",
        "🚀 Клавиша N (Т) — Орбитальный Ядерный удар",
        "⚡ Клавиша J (О) — Заградительная Кассетная мина",
        "--------------------------------------------------",
        "За каждого убитого врага их скорость увеличивается!",
        "Используйте бомбы с умом, чтобы сдерживать натиск."
    ]

    y_offset = 120
    for line in desc_lines:
        if "Клавиша" in line:
            line_surf = font_desc.render(line, True, (255, 255, 0))  # Бомбы подсветим желтым
        elif "---" in line:
            line_surf = font_desc.render(line, True, (0, 150, 255))
        else:
            line_surf = font_desc.render(line, True, (255, 255, 255))

        screen.blit(line_surf, (300 - line_surf.get_width() // 2, y_offset))
        y_offset += 32

    # Кнопка НАЗАД (Тоже центрирована, X = 200 на экране шириной 600)
    rect_back = pygame.Rect(200, 480, 200, 45)
    color_back = (255, 50, 50) if rect_back.collidepoint(mouse_pos) else (180, 40, 40)

    pygame.draw.rect(screen, color_back, rect_back)
    pygame.draw.rect(screen, (255, 255, 255), rect_back, 1)

    txt_s = font_bold.render("Назад", True, (255, 255, 255))
    screen.blit(txt_s, (rect_back.centerx - txt_s.get_width() // 2, rect_back.centery - txt_s.get_height() // 2))

    if click_fired and rect_back.collidepoint(mouse_pos):
        return "MENU"

    return "CONTROLS"