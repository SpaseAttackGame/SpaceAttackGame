import pygame
import random
import time
import math


class Ufo(pygame.sprite.Sprite):
    def __init__(self, screen, stats):
        """Инициализация летающей тарелки Босса"""
        super().__init__()
        self.screen = screen
        self.stats = stats

        # Задаем Боссу ровно 4 ХП при создании
        self.stats.ufo_max_hp = 4
        self.stats.ufo_hp = 4

        # Создаем красный овал для Босса
        self.image = pygame.Surface((60, 25), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 0, 0), (0, 0, 60, 25))

        self.rect = self.image.get_rect()

        # Стартовая позиция
        self.rect.x = -self.rect.width
        self.rect.y = 30
        self.x = float(self.rect.x)
        self.base_y = 30.0  # Базовая высота для синусоиды

        self.speed = 2.0
        self.last_drop_time = time.time()

    def update(self, inos):
        """Движение босса по волнообразной траектории и правильная высадка десанта"""
        # 🟢 Движение по оси X
        self.x += self.speed
        self.rect.x = int(self.x)

        # 🟢 ТРАЕКТОРИЯ: Босс плавно летает вверх-вниз по синусоиде!
        self.rect.y = int(self.base_y + math.sin(self.x / 20) * 15)

        # 🛸 ВЫСАДКА ДЕСАНТА (раз в 2.5 секунды, чтобы не перегружать экран)
        if time.time() - self.last_drop_time > 2.5 and 40 < self.rect.centerx < 460:
            from ino import Ino
            new_ino = Ino(self.screen, self.stats)

            # 1. Сбрасываем флаги здоровья и мутанта
            new_ino.is_mutant = False
            new_ino.health = 1

            # 2. Ставим десантника под летящую тарелку и встраиваем в 3-й ряд
            new_ino.rect.centerx = self.rect.centerx
            new_ino.rect.y = 40 + 30 * 2
            new_ino.x = float(new_ino.rect.x)

            # 3. Синхронизируем направление движения с армией
            if len(inos) > 0:
                new_ino.side = inos.sprites()[0].side
            else:
                new_ino.side = 1

            # Добавляем в общую группу
            inos.add(new_ino)

            self.last_drop_time = time.time()
            print("🪂 ДЕСАНТНИК УСПЕШНО ВСТАЛ В СТРОЙ АРМИИ!")
    def draw_hp_bar(self):
        """Рисует красивую полоску ХП над тарелкой Босса"""
        bar_width = 50
        bar_height = 5
        hp_pct = max(0, self.stats.ufo_hp / self.stats.ufo_max_hp)
        fill_width = int(bar_width * hp_pct)

        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 8

        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))


