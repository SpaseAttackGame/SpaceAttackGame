import pygame
import time

def activate_freeze_bomb(stats):
    """Логика замораживающей бомбы (Клавиша F)"""
    # Запасы уже проверены и списаны в control.py, просто включаем таймер
    stats.freeze_start_time = time.time()
    print("❄️ БОМБА АКТИВИРОВАНА: Пришельцы заморожены на 3 секунды!")
    return True


def activate_nuclear_strike(screen, stats, inos, particles, sc):
    """Логика ядерного удара (Клавиша N)"""
    print("🚀 СБРОС ЯДЕРНОЙ БОМБЫ! Полная зачистка экрана!")

    # Вызываем визуальные эффекты
    from explosion import create_mine_explosion, create_explosion
    create_mine_explosion(screen, (250, 250), particles, is_nuke=True)

    # Считаем очки за каждого пришельца
    points_per_kill = 30 if (hasattr(stats, 'nano_damage') and stats.nano_damage == 1) else 10
    alien_count = len(inos)
    stats.score += alien_count * points_per_kill

    # Маленькие взрывы на месте каждого крабика и полная очистка
    for alien in inos.sprites():
        create_explosion(screen, alien.rect.center, particles, color=(0, 255, 0))

    inos.empty()

    # 🟢 ФИКС ЗАВИСАНИЯ: Безопасное обновление интерфейса
    if hasattr(sc, 'prep_score'):
        sc.prep_score()
    return True


def activate_custom_bomb_j(screen, stats, inos, particles, sc):
    """Логика Кассетной мины на клавишу J (Зачищает нижнюю половину экрана)"""
    import pygame
    import math

    print("⚡ АКТИВИРОВАНА КАССЕТНАЯ МИНА!")

    from explosion import create_mine_explosion, create_explosion
    # Спавним жёлтую взрывную волну чуть ниже центра экрана
    create_mine_explosion(screen, (250, 350), particles, is_nuke=False)

    points_per_kill = 30 if (hasattr(stats, 'nano_damage') and stats.nano_damage == 1) else 10

    # Проверяем пришельцев, которые опустились близко к игроку (ниже Y = 200)
    for alien in inos.copy():
        if alien.rect.y > 200:
            if hasattr(alien, 'is_mutant') and alien.is_mutant:
                alien.health -= 2  # Урон Мутанту
                create_explosion(screen, alien.rect.center, particles, color=(255, 0, 255))
                if alien.health <= 0:
                    alien.kill()
                    inos.remove(alien)
            else:
                # Рядовые враги взрываются жёлтыми искрами
                create_explosion(screen, alien.rect.center, particles, color=(255, 255, 0))
                stats.score += points_per_kill
                alien.kill()
                inos.remove(alien)

    # 🟢 ФИКС ЗАВИСАНИЯ: Безопасное обновление интерфейса
    if hasattr(sc, 'prep_score'):
        sc.prep_score()
    return True