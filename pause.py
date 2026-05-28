import pygame
import sys

def show_pause(screen, stats):
    """Отображает экран паузы и обрабатывает выход или продолжение"""
    font_title = pygame.font.Font(None, 50)
    font_text = pygame.font.Font(None, 30)

    paused = True
    while paused:
        # Рисуем полупрозрачное затемнение
        overlay = pygame.Surface((600, 600)) # Изменил под твой размер экрана 600х600
        overlay.set_alpha(10)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Текст меню паузы
        title_surf = font_title.render("ПАУЗА", True, (255, 255, 0))
        resume_surf = font_text.render("Нажмите 1 — Продолжить игру", True, (255, 255, 255))
        menu_surf = font_text.render("Нажмите 2 — Выйти в главное меню", True, (255, 100, 100))

        # Выводим по центру экрана 600х600
        screen.blit(title_surf, (300 - title_surf.get_width() // 2, 180))
        screen.blit(resume_surf, (300 - resume_surf.get_width() // 2, 260))
        screen.blit(menu_surf, (300 - menu_surf.get_width() // 2, 310))

        pygame.display.flip()

        # Обработка выбора игрока
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    # 🟢 ИСПРАВЛЕНИЕ: Гарантированно отключаем паузу в статистике!
                    stats.game_paused = False
                    return "CONTINUE"
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    # 🟢 ИСПРАВЛЕНИЕ: Сбрасываем паузу и даем команду вернуться в меню!
                    stats.game_paused = False
                    return "TO_MENU"