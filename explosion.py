import pygame
import random
import math


class Particle(pygame.sprite.Sprite):
    """Один пиксель/осколок взрыва"""

    def __init__(self, screen, position, color):
        super().__init__()
        self.screen = screen

        # Случайный размер осколка от 2 до 4 пикселей
        size = random.randint(2, 4)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # Спавним строго в центре погибшего врага
        self.rect.center = position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 🟢 ИСПРАВЛЕННЫЙ РАЗЛЕТ: Распределяем скорость строго по кругу (360 градусов)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 4.5)  # Начальная скорость взрыва
        self.speed_x = math.cos(angle) * speed
        self.speed_y = math.sin(angle) * speed

        # Время жизни осколка в кадрах (примерно полсекунды)
        self.lifetime = random.randint(15, 30)

    def update(self):
        """Движение осколка, физика замедления и его затухание"""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Осколок исчезает навсегда
            return

        # 🟢 ДОБАВЛЕНО ТРЕНИЕ: Осколки плавно замедляются, а не летят бесконечно
        self.speed_x *= 0.92
        self.speed_y *= 0.92

        # Обновляем координаты
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


def create_explosion(screen, position, group, color=(0, 255, 0)):
    """Создает аккуратную вспышку частиц в месте взрыва"""
    for _ in range(random.randint(12, 20)):
        particle = Particle(screen, position, color)
        group.add(particle)


def create_bunker_explosion(screen, position, group):
    """Создает сочный взрыв при уничтожении блока бункера"""
    # Создаем 10-15 крупных тяжелых осколков зеленого цвета
    for _ in range(random.randint(10, 15)):
        particle = Particle(screen, position, color=(0, 255, 0))
        # Сделаем осколки бункера чуть медленнее, чтобы они тяжело осыпались
        particle.speed_x *= 0.7
        particle.speed_y *= 0.7
        group.add(particle)


class MineParticle(pygame.sprite.Sprite):
    """Осколок от взрыва мины/ядерной бомбы, летящий по расширяющемуся радиусу"""

    def __init__(self, screen, position, color, max_radius):
        super().__init__()
        self.screen = screen

        # Осколки ядерной бомбы крупнее обычных (от 3 до 5 пикселей)
        size = random.randint(3, 5)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # Начальная точка — центр экрана (откуда идёт волна)
        self.start_x, self.start_y = position
        self.rect.center = position

        # Направление движения (угол разлёта по кругу)
        self.angle = random.uniform(0, 2 * math.pi)
        self.max_radius = max_radius
        self.lifetime = random.randint(25, 35)
        self.speed = self.max_radius / self.lifetime * random.uniform(0.8, 1.2)

        self.current_radius = 0.0

    def update(self):
        """Расширение радиуса взрыва и исчезновение"""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            return

        # Увеличиваем радиус волны
        self.current_radius += self.speed

        # Считаем новые координаты по кругу от центра
        new_x = self.start_x + math.cos(self.angle) * self.current_radius
        new_y = self.start_y + math.sin(self.angle) * self.current_radius

        self.rect.centerx = int(new_x)
        self.rect.centery = int(new_y)


def create_mine_explosion(screen, position, group, is_nuke=False):
    """Создает мощную ударную круговую волну частиц на весь экран"""
    # 💥 Настройки для ураганной ядерной бомбы
    radius = 250  # Радиус волны на весь экран 500x500
    color = (255, 140, 0)  # Огненно-оранжевый цвет ядерного взрыва
    particle_count = 70  # Количество частиц для сочного эффекта

    for _ in range(particle_count):
        particle = MineParticle(screen, position, color, radius)
        group.add(particle)