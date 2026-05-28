import pygame


class Ino(pygame.sprite.Sprite):
    def __init__(self, screen, stats):
        """Инициализация одного пришельца"""
        super(Ino, self).__init__()
        self.screen = screen
        self.stats = stats  # Связь со статистикой для магазина

        # Загружаем картинку с зеленым крабиком
        self.image = pygame.image.load('pixil-frame-0 (1).png')
        self.image = pygame.transform.scale(self.image, (26, 20))
        self.rect = self.image.get_rect()

        # Физические координаты для плавного движения по обеим осям
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 🛸 ФЛАГ НАПРАВЛЕНИЯ: 1 — вправо, -1 — влево
        self.side = 1

    def update(self, alien_speed):
        """Перемещает пришельца вправо или влево на основе переданной скорости"""
        # Сдвигаем физическую координату X
        self.x += (alien_speed * 0.5) * self.side
        self.rect.x = int(self.x)

        # Жестко синхронизируем Y, чтобы пришельцы держались в своих рядах
        self.rect.y = int(self.y)