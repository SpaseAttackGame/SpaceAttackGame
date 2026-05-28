import pygame
import time
import math
from ino import Ino


def create_army(screen, inos, stats):
    """Создает ОГРОМНУЮ плотную армию пришельцев для хардкорного боя!"""
    number_inos_x = 14
    number_rows = 9

    for row_number in range(number_rows):
        for ino_number in range(number_inos_x):
            # Строку "from ino import Ino" отсюда полностью УДАЛИЛИ!
            new_ino = Ino(screen, stats)

            # Устанавливаем координаты прямоугольника
            new_ino.rect.x = 30 + 30 * ino_number
            new_ino.rect.y = 35 + 22 * row_number

            # Физические координаты для класса Ino
            new_ino.x = float(new_ino.rect.x)
            new_ino.y = float(new_ino.rect.y)
            new_ino.side = 1

            # Делаем первого пришельца Гигантским Мутантом
            if row_number == 0 and ino_number == 0 and hasattr(stats, 'spawn_mutant') and stats.spawn_mutant == 1:
                new_ino.image = pygame.transform.scale(new_ino.image, (78, 60))
                old_center = new_ino.rect.center
                new_ino.rect = new_ino.image.get_rect()
                new_ino.rect.center = old_center

                new_ino.health = 5
                new_ino.is_mutant = True
                print("Alien Мутант заспавнялся!")
            else:
                new_ino.health = 1
                new_ino.is_mutant = False

            inos.add(new_ino)


def update(bg_color, screen, stats, sc, gun, inos, bullets, particles, bunkers=None, ufo_group=None):
    """Отрисовывает все элементы игры на экране и ГАРАНТИРОВАННО обновляет табло счёта"""

    # 🟢 ЖЕЛЕЗНЫЙ ФИКС ОБНОВЛЕНИЯ СЧЁТА:
    # Заставляем Scores пересчитывать новые очки перед каждым выводом на экран
    if hasattr(sc, 'prep_score'):
        sc.prep_score()
    elif hasattr(sc, 'image_score'):
        sc.image_score()
    elif hasattr(sc, 'prep_images'):
        sc.prep_images()

    # Очищаем экран под новую отрисовку кадра (теперь стоит ровно и без условий!)
    screen.fill(bg_color)

    # 1. Рисуем пули
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 2. Рисуем защитный щит вокруг пушки
    if hasattr(stats, 'shield') and stats.shield == 1:
        pygame.draw.circle(screen, (0, 255, 255), gun.rect.center, 45, 3)

    # 3. Выводим пушку и пришельцев
    gun.output()
    inos.draw(screen)

    # 4. Выводим защитные бункеры
    if bunkers:
        for block in bunkers.sprites():
            if hasattr(block, 'update_color'):
                block.update_color()
        bunkers.draw(screen)

    # 5. Частицы взрывов
    particles.draw(screen)

    # 6. Босс UFO и его полоска здоровья
    if ufo_group and len(ufo_group) > 0:
        ufo_group.draw(screen)
        for boss in ufo_group.sprites():
            if hasattr(boss, 'draw_hp_bar'):
                boss.draw_hp_bar()

    # 7. Выводим счёт и обновляем кадр на экране
    sc.show_score()
    pygame.display.flip()

def update_bullets(screen, stats, sc, inos, bullets, alien_speed, particles, ufo_group=None, hit_sound=None):
    """Обновляет позиции пуль, начисляет очки и обрабатывает попадания"""
    bullets.update()

    destroy_bullet_on_hit = False if (hasattr(stats, 'pierce_shot') and stats.pierce_shot == 1) else True
    collisions = pygame.sprite.groupcollide(bullets, inos, False, False)

    if collisions:
        if hit_sound:
            hit_sound.play()
        for bullet, inos_hit in collisions.items():
            for ino in inos_hit:
                if bullet not in bullets:
                    continue

                if hasattr(ino, 'is_mutant') and ino.is_mutant:
                    ino.health -= 1
                    if destroy_bullet_on_hit:
                        bullet.kill()
                    if ino.health > 0:
                        continue

                from explosion import create_explosion
                if hasattr(ino, 'is_mutant') and ino.is_mutant:
                    create_explosion(screen, ino.rect.center, particles, color=(255, 0, 255))

                    from bullet import Bullet
                    for i in range(10):
                        fragment = Bullet(screen, gun=None, stats=stats)
                        fragment.rect.center = ino.rect.center
                        fragment.y = float(fragment.rect.y)

                        angle = math.radians(i * 365 / 10)
                        fragment.speed_x = math.cos(angle) * 10.0
                        fragment.speed_y = math.sin(angle) * 10.0

                        def fragment_update(frag=fragment):
                            frag.rect.x += int(frag.speed_x)
                            frag.y += frag.speed_y
                            frag.rect.y = int(frag.y)

                        fragment.update = fragment_update
                        bullets.add(fragment)
                else:
                    create_explosion(screen, ino.rect.center, particles, color=(0, 255, 0))

                points_per_kill = 30 if (hasattr(stats, 'nano_damage') and stats.nano_damage == 1) else 10
                stats.score += points_per_kill
                inos.remove(ino)

                if hasattr(stats, 'current_weapon') and stats.current_weapon == "railgun":
                    if not hasattr(bullet, 'pierce_count'):
                        bullet.pierce_count = 3
                    bullet.pierce_count -= 1
                    if bullet.pierce_count <= 0:
                        bullet.kill()
                else:
                    if destroy_bullet_on_hit:
                        bullet.kill()

    # Попадания по Боссу-UFO
    if ufo_group and stats.ufo_active:
        boss_collisions = pygame.sprite.groupcollide(bullets, ufo_group, True, False)
        if boss_collisions:
            stats.ufo_hp -= 1
            if stats.ufo_hp <= 0:
                from explosion import create_explosion
                for boss in ufo_group.sprites():
                    create_explosion(screen, boss.rect.center, particles, color=(255, 69, 0))
                stats.score += 1500
                ufo_group.empty()
                stats.ufo_active = False
                stats.ufo_last_spawn = time.time()
                if hasattr(sc, 'image_score'): sc.image_score()

    # Очистка вылетевших пуль
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0 or bullet.rect.top >= 600:
            bullets.remove(bullet)

    if len(inos) == 0:
        bullets.empty()
        alien_speed += 0.1
        create_army(screen, inos, stats)

    # 🔥 ГАРАНТИРОВАННЫЙ ВОЗВРАТ СКОРОСТИ
    return alien_speed
def check_army_edges(screen, inos):
    """Проверяет, дошли ли пришельцы до краев экрана"""
    for ino in inos.sprites():
        if ino.side == 1 and ino.rect.right >= 600:
            return True
        elif ino.side == -1 and ino.rect.left <= 0:
            return True
    return False


def change_army_direction(screen, inos):
    """Сдвигает армию вниз и меняет направление движения"""
    for ino in inos.sprites():
        ino.rect.y += 10
        ino.side *= -1
        if ino.side == -1:
            ino.rect.x -= 6
        else:
            ino.rect.x += 6
        ino.x = float(ino.rect.x)
        ino.y = float(ino.rect.y)


def update_inos(stats, screen, sc, gun, inos, bullets, alien_speed, particles, ufo_group=None, bunkers=None):
    """Главная функция обновления пришельцев во время игры с плавным дробным ускорением"""
    if ufo_group and stats.ufo_active:
        ufo_group.update(inos)
        for boss in ufo_group.sprites():
            if boss.rect.x > 550:
                ufo_group.empty()
                stats.ufo_active = False
                stats.ufo_last_spawn = time.time()
                print("🛸 Босс улетел невредимым!")

    # Если работает заморозка — армия стоит на месте
    if hasattr(stats, 'freeze_start_time') and time.time() - stats.freeze_start_time < 3:
        inos_check(stats, screen, sc, gun, inos, bullets, particles, ufo_group, bunkers)
        return

    if check_army_edges(screen, inos):
        change_army_direction(screen, inos)

    # 👥 Считаем, сколько пришельцев уже убито в этой волне:
    max_aliens = 126
    current_aliens = len(inos)
    killed_aliens = max(0, max_aliens - current_aliens)

    # 🔥 УВЕЛИЧИВАЕМ ШАГ УСКОРЕНИЯ: за каждого убитого прибавляем 0.02 пикселя.
    # Когда останется мало врагов, они будут летать как бешеные!
    dynamic_speed = alien_speed + (killed_aliens * 0.02)

    # 🟢 ЖЕСТКИЙ ФИКС ДВИЖЕНИЯ ПО ДРОБНЫМ КООРДИНАТАМ:
    # Вместо встроенного inos.update двигаем каждого пришельца вручную через его float-переменную self.x
    for ino in inos.sprites():
        # Меняем дробную координату пришельца
        ino.x += dynamic_speed * ino.side
        # Переносим дробное значение в физический хитбокс на экране
        ino.rect.x = int(ino.x)

    inos_check(stats, screen, sc, gun, inos, bullets, particles, ufo_group, bunkers)


def inos_check(stats, screen, sc, gun, inos, bullets, particles, ufo_group, bunkers):
    """Проверка столкновения пришельцев с пушкой и бункерами с учетом ЩИТА"""
    if bunkers:
        bunker_collisions = pygame.sprite.groupcollide(inos, bunkers, False, False)

        if bunker_collisions:
            from explosion import create_bunker_explosion
            bunker_explosion_radius = 70

            for alien, hit_bunkers in bunker_collisions.items():
                for block in hit_bunkers:
                    target_center = block.rect.center

                    for target_block in bunkers.copy():
                        distance = math.hypot(
                            target_block.rect.centerx - target_center[0],
                            target_block.rect.centery - target_center[1]
                        )

                        if distance <= bunker_explosion_radius:
                            create_bunker_explosion(screen, target_block.rect.center, particles)
                            target_block.kill()

                points_per_kill = 30 if (hasattr(stats, 'nano_damage') and stats.nano_damage == 1) else 10
                stats.score += points_per_kill
                alien.kill()

    hit_alien = pygame.sprite.spritecollideany(gun, inos)

    if hit_alien:
        if hasattr(stats, 'shield') and stats.shield == 1:
            stats.shield = 0
            print("💥 ЩИТ ВЗОРВАЛСЯ! Текущая волна уничтожена!")
            inos.empty()
            stats.score += 1000
            if hasattr(sc, 'prep_score'): sc.prep_score()
            elif hasattr(sc, 'image_score'): sc.image_score()

            from explosion import create_explosion
            screen_rect = screen.get_rect()
            create_explosion(screen, screen_rect.center, particles, color=(0, 255, 255))
            return
        else:
            restart_level_after_crash(stats, screen, sc, gun, inos, bullets, bunkers, ufo_group)


def events(event, screen, gun, bullets, stats, inos, particles, sc):
    """Полный обработчик ввода: ловит одиночные нажатия бомб и удержание клавиш движения"""
    current_time = time.time()

    # --- ЧАСТЬ 1: Одиночные нажатия клавиш (Бомбы, Оружие, Пауза) ---
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p:
            if not hasattr(stats, 'game_paused'):
                stats.game_paused = False
            stats.game_paused = not stats.game_paused
            print(f"⏸️ Пауза: {stats.game_paused}")

        elif event.key == pygame.K_1:
            stats.current_weapon = "plasma"
            print("🧪 Выбран: Плазменный залп")

        elif event.key == pygame.K_2:
            has_rail = getattr(stats, 'has_railgun', 0) == 1 or getattr(stats, 'pierce_shot', 0) == 1
            if has_rail:
                stats.current_weapon = "railgun"
                print("⚡ Выбран: Сквозной Рельсотрон")
            else:
                print("❌ Рельсотрон еще не куплен в магазине!")

        # --- БОМБА ЗАМОРОЗКИ (Клавиша F или А) ---
        elif event.key == pygame.K_f or event.unicode.lower() in ['f', 'а']:
            print("❄️ БОМБА АКТИВИРОВАНА: Заморозка!")
            stats.freeze_start_time = current_time

            # Глушим фоновые звуки и воспроизводим активацию заморозки
            pygame.mixer.stop()
            try:
                bomb_channel = pygame.mixer.Channel(1)
                bomb_sound = pygame.mixer.Sound("bomb.mp3")  # Замени на свой файл звука, когда скачаешь!
                bomb_channel.set_volume(1.0)
                bomb_channel.play(bomb_sound)
            except:
                pass

        # --- ЯДЕРНЫЙ УДАР (Клавиша N или Т) ---
        elif event.key == pygame.K_n or event.unicode.lower() in ['n', 'т']:
            print("🚀 ЯДЕРНЫЙ УДАР: Полная зачистка!")

            # ЖЕСТКИЙ ФИКС ЗВУКА: обрываем писки обычных смертей и взрываем на 100% громкости
            pygame.mixer.stop()
            try:
                bomb_channel = pygame.mixer.Channel(1)
                bomb_sound = pygame.mixer.Sound("bomb.mp3")  # Сюда можно прописать "bomb.mp3"
                bomb_channel.set_volume(1.0)
                bomb_channel.play(bomb_sound)
            except Exception as e:
                print(f"Ошибка звука бомбы: {e}")

            from explosion import create_mine_explosion, create_explosion
            create_mine_explosion(screen, (250, 250), particles, is_nuke=True)
            points_per_kill = 30 if (hasattr(stats, 'nano_damage') and stats.nano_damage == 1) else 10
            stats.score += len(inos) * points_per_kill

            for alien in inos.sprites():
                create_explosion(screen, alien.rect.center, particles, color=(0, 255, 0))
            inos.empty()
            if hasattr(sc, 'prep_score'): sc.prep_score()

        # --- КАССЕТНАЯ МИНА (Клавиша J или О) ---
        elif event.key == pygame.K_j or event.unicode.lower() in ['j', 'о']:
            print("⚡ КАССЕТНАЯ МИНА: Очистка низа!")

            # ЖЕСТКИЙ ФИКС ЗВУКА: глушим мелкие звуки, давая приоритет мине
            pygame.mixer.stop()
            try:
                bomb_channel = pygame.mixer.Channel(1)
                bomb_sound = pygame.mixer.Sound("bomb.mp3")  # Сюда можно прописать "mine.mp3"
                bomb_channel.set_volume(1.0)
                bomb_channel.play(bomb_sound)
            except Exception as e:
                print(f"Ошибка звука мины: {e}")

            from explosion import create_mine_explosion, create_explosion
            create_mine_explosion(screen, (250, 350), particles, is_nuke=False)
            points_per_kill = 30 if (hasattr(stats, 'nano_damage') and stats.nano_damage == 1) else 10

            for alien in inos.copy():
                if alien.rect.y > 200:
                    if hasattr(alien, 'is_mutant') and alien.is_mutant:
                        alien.health -= 2
                        create_explosion(screen, alien.rect.center, particles, color=(255, 0, 255))
                        if alien.health <= 0:
                            alien.kill()
                            inos.remove(alien)
                    else:
                        create_explosion(screen, alien.rect.center, particles, color=(255, 255, 0))
                        stats.score += points_per_kill
                        alien.kill()
                        inos.remove(alien)
            if hasattr(sc, 'prep_score'): sc.prep_score()

    # --- ЧАСТЬ 2: Постоянное удержание клавиш (Движение и стрельба пробелом) ---
    if getattr(stats, 'game_paused', False):
        gun.mright = False
        gun.mleft = False
        return

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        gun.mright = True
        gun.mleft = False
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        gun.mleft = True
        gun.mright = False
    else:
        gun.mright = False
        gun.mleft = False

    if keys[pygame.K_SPACE]:
        plasma_lvl = getattr(stats, 'plasma_size', 1)
        delay = 0.42 - (plasma_lvl * 0.05) if plasma_lvl > 1 else 0.45

        if not hasattr(stats, 'last_shot_time') or current_time - stats.last_shot_time > delay:
            fire_bullet(screen, gun, bullets, stats)
            stats.last_shot_time = current_time

def fire_bullet(screen, gun, bullets, stats):
    """Создает снаряд в зависимости от выбранного оружия с авто-коррекцией хитбокса"""
    current_time = time.time()
    new_bullet = None
    from bullet import Bullet

    if stats.current_weapon == "laser":
        new_bullet = Bullet(screen, gun, stats)
        new_bullet.image = pygame.Surface((3, 12))
        new_bullet.image.fill((255, 255, 255))
        stats.pierce_shot = 0

    elif stats.current_weapon == "plasma":
        if stats.plasma_mode == "ready":
            stats.plasma_mode = "shooting"
            stats.plasma_timer_start = current_time
        if stats.plasma_mode == "shooting" and current_time - stats.plasma_timer_start > 2.0:
            stats.plasma_mode = "recharging"
            stats.plasma_timer_start = current_time
        if stats.plasma_mode == "recharging" and current_time - stats.plasma_timer_start > 5.0:
            stats.plasma_mode = "ready"

        new_bullet = Bullet(screen, gun, stats)
        stats.pierce_shot = 0

        size_lvl = 1 if stats.plasma_mode == "recharging" else getattr(stats, 'plasma_size', 1)
        bullet_width = 3 + (size_lvl - 1) * 8

        new_bullet.image = pygame.Surface((bullet_width, 12))
        new_bullet.image.fill((0, 255, 0))

    elif stats.current_weapon == "railgun":
        last_time = getattr(stats, 'last_rail_time', 0.0)
        if current_time - last_time < 0.6:
            return

        stats.last_rail_time = current_time
        new_bullet = Bullet(screen, gun, stats)
        stats.pierce_shot = 1
        new_bullet.image = pygame.Surface((2, 24))
        new_bullet.image.fill((255, 0, 255))

    if new_bullet is not None:
        # 🔥 ФИКС ЦЕНТРИРОВАНИЯ И ХИТБОКСА ПЛАЗМЫ:
        new_bullet.rect = new_bullet.image.get_rect()
        if gun:
            new_bullet.rect.centerx = gun.rect.centerx
            new_bullet.rect.top = gun.rect.top

        new_bullet.y = float(new_bullet.rect.y)
        bullets.add(new_bullet)

def restart_level_after_crash(stats, screen, sc, gun, inos, bullets, bunkers, ufo_group):
    """Перезапуск уровня при потере жизни или вызов Game Over"""
    if getattr(stats, 'guns_left', 0) > 1:
        stats.guns_left -= 1
        if hasattr(sc, 'prep_guns'): sc.prep_guns()
        elif hasattr(sc, 'image_guns'): sc.image_guns()

        inos.empty()
        bullets.empty()
        if ufo_group:
            ufo_group.empty()
            stats.ufo_active = False
            stats.ufo_last_spawn = time.time()

        create_army(screen, inos, stats)

        gun.rect.centerx = 300
        gun.rect.bottom = 550
        gun.x = float(gun.rect.centerx)
        gun.center = float(gun.rect.centerx)
        time.sleep(1.0)
    else:
        show_game_over(screen, stats)
        stats.plasma_mode = "ready"


def show_game_over(screen, stats):
    """Красивый экран окончания игры"""
    screen.fill((0, 0, 0))
    font_title = pygame.font.Font(None, 50)
    font_text = pygame.font.Font(None, 35)

    title_surf = font_title.render("GAME OVER", True, (255, 0, 0))
    score_surf = font_text.render(f"Ваш счет: {stats.score}", True, (255, 255, 255))

    screen.blit(title_surf, (300 - title_surf.get_width() // 2, 220))
    screen.blit(score_surf, (300 - score_surf.get_width() // 2, 300))
    pygame.display.flip()

    time.sleep(3)
    stats.reset_stats()
    stats.run_game = False
    pygame.mouse.set_visible(True)


def activate_custom_bomb_j(screen, stats, inos, particles, sc):
    """Логика Кассетной мины на клавишу J"""
    cluster_bombs = getattr(stats, 'cluster_bombs', 0)
    if cluster_bombs > 0:
        stats.cluster_bombs -= 1
        print(f"⚡ АКТИВИРОВАНА КАССЕТНАЯ МИНА! Осталось: {stats.cluster_bombs}")

        from explosion import create_mine_explosion, create_explosion
        create_mine_explosion(screen, (300, 450), particles, is_nuke=False)

        points_per_kill = 30 if (hasattr(stats, 'nano_damage') and stats.nano_damage == 1) else 10

        for alien in inos.copy():
            if alien.rect.y > 250:
                if hasattr(alien, 'is_mutant') and alien.is_mutant:
                    alien.health -= 2
                    create_explosion(screen, alien.rect.center, particles, color=(255, 0, 255))
                    if alien.health <= 0:
                        def restart_level_after_crash(stats, screen, sc, gun, inos, bullets, bunkers, ufo_group):
                            """Перезапуск уровня при потере жизни корабля или вызов Game Over"""
                            if getattr(stats, 'guns_left', 0) > 1:
                                stats.guns_left -= 1
                                if hasattr(sc, 'prep_guns'):
                                    sc.prep_guns()
                                elif hasattr(sc, 'image_guns'):
                                    sc.image_guns()

                                inos.empty()
                                bullets.empty()
                                if ufo_group:
                                    ufo_group.empty()
                                    stats.ufo_active = False
                                    stats.ufo_last_spawn = time.time()

                                create_army(screen, inos, stats)

                                gun.rect.centerx = 300
                                gun.rect.bottom = 550
                                gun.x = float(gun.rect.centerx)
                                gun.center = float(gun.rect.centerx)
                                time.sleep(1.0)
                            else:
                                show_game_over(screen, stats)
                                stats.plasma_mode = "ready"
def show_game_over(screen, stats):
    """Красивый экран окончания игры с выводом финального счета"""
    screen.fill((0, 0, 0))
    font_title = pygame.font.Font(None, 50)
    font_text = pygame.font.Font(None, 35)

    title_surf = font_title.render("GAME OVER", True, (255, 0, 0))
    score_surf = font_text.render(f"Ваш счет: {stats.score}", True, (255, 255, 255))

    screen.blit(title_surf, (300 - title_surf.get_width() // 2, 220))
    screen.blit(score_surf, (300 - score_surf.get_width() // 2, 300))
    pygame.display.flip()

    time.sleep(3)
    stats.reset_stats()
    stats.run_game = False
    pygame.mouse.set_visible(True)

def activate_custom_bomb_j(screen, stats, inos, particles, sc):
    """Логика Кассетной мины на клавишу J (Зачищает нижнюю половину экрана)"""
    cluster_bombs = getattr(stats, 'cluster_bombs', 0)
    if cluster_bombs > 0:
        stats.cluster_bombs -= 1
        print(f"⚡ АКТИВИРОВАНА КАССЕТНАЯ МИНА! Осталось: {stats.cluster_bombs}")

        from explosion import create_mine_explosion, create_explosion
        create_mine_explosion(screen, (300, 450), particles, is_nuke=False)

        points_per_kill = 30 if (hasattr(stats, 'nano_damage') and stats.nano_damage == 1) else 10

        for alien in inos.copy():
            if alien.rect.y > 250:
                if hasattr(alien, 'is_mutant') and alien.is_mutant:
                    alien.health -= 2
                    create_explosion(screen, alien.rect.center, particles, color=(255, 0, 255))
                    if alien.health <= 0:
                        alien.kill()
                        inos.remove(alien)
                else:
                    create_explosion(screen, alien.rect.center, particles, color=(255, 255, 0))
                    stats.score += points_per_kill
                    alien.kill()
                    inos.remove(alien)

        if hasattr(sc, 'prep_score'):
            sc.prep_score()
        elif hasattr(sc, 'image_score'):
            sc.image_score()
        return True
    else:
        print("❌ У вас нет Кассетных мин! Купите их в магазине.")
        return False