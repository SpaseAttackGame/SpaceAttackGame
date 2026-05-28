import pygame
import sys
import random
import math
import time

def show_shop(screen, stats, sc):
    """Отображает космический магазин, адаптированный под экран 600x600 с бесконечными звездами"""
    font_title = pygame.font.Font(None, 42)
    font_text = pygame.font.Font(None, 24)
    font_tip = pygame.font.Font(None, 18)

    # Позиционирование ячейки промокода под размер 600x600
    promo_text = ""
    promo_box = pygame.Rect(40, 510, 250, 32)
    promo_message = "Введите промокод и нажмите ENTER"
    promo_msg_color = (130, 140, 160)

    # Интерьер: Создаем 40 случайных бесконечно падающих звезд для фона магазина
    shop_stars = []
    for _ in range(40):
        shop_stars.append({
            'x': random.randint(10, 590),
            'y': random.randint(10, 590),
            'speed': random.uniform(0.4, 1.2),
            'size': random.randint(1, 2)
        })

    in_shop = True
    clock = pygame.time.Clock()

    while in_shop:
        # Глубокий космический цвет заливки
        screen.fill((5, 8, 26))

        # Отрисовка и движение звездного неба
        for star in shop_stars:
            star['y'] += star['speed']
            if star['y'] >= 600:
                star['y'] = 0
                star['x'] = random.randint(10, 590)
                star['speed'] = random.uniform(0.4, 1.2)

            pygame.draw.circle(screen, (220, 230, 255), (int(star['x']), int(star['y'])), star['size'])

        # Заголовки (Отцентрированы по центру 300)
        title_surf = font_title.render("🛸 К О С М И Ч Е С К И Й  А Р С Е Н А Л 🛸", True, (0, 255, 255))
        score_surf = font_text.render(f"Ваш бюджет: {stats.score} 💰", True, (255, 255, 0))
        screen.blit(title_surf, (300 - title_surf.get_width() // 2, 25))
        screen.blit(score_surf, (300 - score_surf.get_width() // 2, 65))

        # Двойная неоновая линия под заголовком
        pygame.draw.line(screen, (0, 150, 255), (35, 90), (565, 90), 1)
        pygame.draw.line(screen, (0, 255, 255), (70, 90), (530, 90), 2)

        # Данные товаров в магазине
        products = [
            (f"1. Двойной выстрел [Lvl: {stats.double_shot}/2]", stats.double_shot_cost, stats.double_shot >= 2),
            (f"2. Ширина плазмы [Lvl: {stats.plasma_size}/5]", stats.plasma_size_cost, stats.plasma_size >= 5),
            (f"3. Энергетический щит [Куплен: {'ДА' if stats.shield else 'НЕТ'}]", stats.shield_cost, stats.shield),
            (f"4. Бомба заморозки [Штук: {stats.time_freeze_ammo}/5]", stats.time_freeze_cost, stats.time_freeze_ammo >= 5),
            (f"5. Сквозной рельсотрон [Куплен: {'ДА' if stats.pierce_shot else 'НЕТ'}]", stats.pierce_cost, stats.pierce_shot),
            (f"6. Ядовитая бомба [Штук: {stats.nuke_bombs}/5]", stats.nuke_cost, stats.nuke_bombs >= 5),
            (f"7. Кассетная мина [Штук: {getattr(stats, 'cluster_bombs', 0)}/5]", 600, getattr(stats, 'cluster_bombs', 0) >= 5)
        ]

        # Отрисовка подложек и неоновых звезд товаров
        y_pos = 105
        for label, cost, is_max in products:
            item_rect = pygame.Rect(35, y_pos, 530, 34)

            if is_max:
                bg_color = (20, 35, 30)
                border_color = (0, 200, 100)
                text_color = (150, 255, 150)
                display_text = f"{label} [МАКСИМУМ]"
                star_color = (255, 215, 0)
            elif stats.score >= cost:
                bg_color = (15, 30, 55)
                border_color = (0, 150, 255)
                text_color = (255, 255, 255)
                display_text = f"{label} — Цена: {cost} 💰"

                pulse = int((math.sin(time.time() * 6) + 1) * 45)
                star_color = (0, 165 + pulse, 255)
            else:
                bg_color = (25, 20, 30)
                border_color = (150, 50, 50)
                text_color = (180, 160, 160)
                display_text = f"{label} — Цена: {cost} ❌"
                star_color = (90, 95, 110)

            pygame.draw.rect(screen, bg_color, item_rect)
            pygame.draw.rect(screen, border_color, item_rect, 1)

            # Отрисовка декоративного неонового крестика-звездочки
            star_center = (item_rect.x + 18, item_rect.y + 17)
            cx, cy = star_center
            pygame.draw.line(screen, star_color, (cx - 6, cy), (cx + 6, cy), 2)
            pygame.draw.line(screen, star_color, (cx, cy - 6), (cx, cy + 6), 2)

            surf = font_text.render(display_text, True, text_color)
            screen.blit(surf, (item_rect.x + 38, item_rect.y + 7))
            y_pos += 42

        # Отрисовка ячейки ввода промокода
        pygame.draw.rect(screen, (0, 255, 255), promo_box, 1)
        txt_surface = font_text.render(promo_text, True, (255, 255, 255))
        screen.blit(txt_surface, (promo_box.x + 10, promo_box.y + 6))

        msg_surface = font_tip.render(promo_message, True, promo_msg_color)
        screen.blit(msg_surface, (promo_box.right + 15, promo_box.y + 8))

        # Подсказка для выхода
        tip_surf = font_tip.render("Нажмите ESC или ПРАВУЮ кнопку мыши для возвращения на орбиту", True, (0, 150, 200))
        screen.blit(tip_surf, (300 - tip_surf.get_width() // 2, 560))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Нажатие правой кнопки мыши — выход на орбиту
                    in_shop = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_shop = False

                # Товар 1: Двойной выстрел
                elif event.key in [pygame.K_1, pygame.K_KP1]:
                    if stats.score >= stats.double_shot_cost and stats.double_shot < 2:
                        stats.score -= stats.double_shot_cost
                        stats.double_shot += 1
                        promo_message = "🛒 Куплен Двойной выстрел!"
                        promo_msg_color = (0, 255, 0)
                    continue

                # Товар 2: Ширина плазмы
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    if stats.score >= stats.plasma_size_cost and stats.plasma_size < 5:
                        stats.score -= stats.plasma_size_cost
                        stats.plasma_size += 1
                        stats.has_plasma = 1
                        stats.plasma_size_cost += 200
                        promo_message = "🛒 Улучшена Ширина плазмы!"
                        promo_msg_color = (0, 255, 0)
                    continue

                # Товар 3: Энергетический щит
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    if stats.score >= stats.shield_cost and not stats.shield:
                        stats.score -= stats.shield_cost
                        stats.shield = 1
                        promo_message = "🛡️ Энергетический щит активирован!"
                        promo_msg_color = (0, 255, 255)
                    continue

                # Товар 4: Бомба заморозки
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    if stats.time_freeze_ammo >= 5:
                        promo_message = "❌ Достигнут лимит Бомб заморозки (макс 5)!"
                        promo_msg_color = (255, 100, 100)
                    elif stats.score >= stats.time_freeze_cost:
                        stats.score -= stats.time_freeze_cost
                        stats.time_freeze_ammo += 1
                        promo_message = "🛒 Куплена Бомба заморозки!"
                        promo_msg_color = (0, 255, 0)
                    continue

                # Товар 5: Сквозной рельсотрон
                elif event.key in [pygame.K_5, pygame.K_KP5]:
                    cost_to_check = getattr(stats, 'pixel_cost', stats.pierce_cost)
                    if stats.score >= cost_to_check and not stats.pierce_shot:
                        stats.score -= stats.pierce_cost
                        stats.pierce_shot = 1
                        stats.has_railgun = 1
                        promo_message = "⚡ Рельсотрон добавлен в арсенал!"
                        promo_msg_color = (0, 255, 255)
                    continue

                # Товар 6: Ядовитая/Ядерная бомба
                elif event.key in [pygame.K_6, pygame.K_KP6]:
                    if stats.nuke_bombs >= 5:
                        promo_message = "❌ Достигнут лимит Ядовитых бомб (макс 5)!"
                        promo_msg_color = (255, 100, 100)
                    elif stats.score >= stats.nuke_cost:
                        stats.score -= stats.nuke_cost
                        stats.nuke_bombs += 1
                        promo_message = "🛒 Куплена Ядовитая бомба!"
                        promo_msg_color = (0, 255, 0)
                    continue

                # Товар 7: Кассетная мина
                elif event.key in [pygame.K_7, pygame.K_KP7]:
                    if not hasattr(stats, 'cluster_bombs'):
                        stats.cluster_bombs = 0
                    if stats.cluster_bombs >= 5:
                        promo_message = "❌ Достигнут лимит Кассетных мин (макс 5)!"
                        promo_msg_color = (255, 100, 100)
                    elif stats.score >= 600:
                        stats.score -= 600
                        stats.cluster_bombs += 1
                        promo_message = f"🛒 Куплена Кассетная мина! Штук: {stats.cluster_bombs}"
                        promo_msg_color = (0, 255, 0)
                    continue

                # Нажатие ENTER — Проверка промокода
                elif event.key == pygame.K_RETURN:
                    current_code = promo_text.upper()

                    if current_code == "CHEAT5000":
                        stats.score += 5000
                        promo_message = "✅ +5000 очков начислено!"
                        promo_msg_color = (0, 255, 0)
                    elif current_code == "MEGAMONEY":
                        stats.score += 8500
                        promo_message = "💰 МЕГА-БАЛАНС: +8 500 очков!"
                        promo_msg_color = (255, 215, 0)
                    elif current_code == "ULTIMATE":
                        stats.score += 50000
                        stats.nuke_bombs = 5
                        stats.time_freeze_ammo = 5
                        stats.cluster_bombs = 5
                        stats.double_shot = 2
                        stats.plasma_size = 5
                        stats.pierce_shot = 1
                        stats.has_plasma = 1
                        stats.has_railgun = 1
                        promo_message = "👑 ULTIMATE: Арсенал полностью укомплектован!"
                        promo_msg_color = (0, 255, 255)
                    else:
                        promo_message = "❌ Неверный промокод!"
                        promo_msg_color = (255, 0, 0)

                    promo_text = ""
                    continue

                # Нажатие Backspace — Стереть букву
                elif event.key == pygame.K_BACKSPACE:
                    promo_text = promo_text[:-1]
                    continue

                # Ввод букв и цифр в поле промокода
                if len(promo_text) < 14 and event.unicode.isalnum():
                    promo_text += event.unicode

        clock.tick(60)

        # 🟢 БЕЗОПАСНЫЙ ФИКС: Обновляем очки без вызова зависающего метода sc.image_score()
        if hasattr(sc, 'prep_score'):
            sc.prep_score()
        elif hasattr(sc, 'show_score'):
            # Если нет prep_score, интерфейс сам подтянет новые очки из stats.score при отрисовке кадра
            pass