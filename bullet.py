import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, gun, stats):
        """Создает объект пули в текущей позиции пушки"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.stats = stats

        # Определяем ширину плазмы на основе прокачки из магазина
        size_lvl = getattr(stats, 'plasma_size', 1)
        bullet_width = 3 + (size_lvl - 1) * 8

        # Создаем форму пули динамически
        if hasattr(stats, 'current_weapon') and stats.current_weapon == "railgun":
            self.image = pygame.Surface((2, 24))
            self.image.fill((255, 0, 255))  # Розовая рельса
        else:
            self.image = pygame.Surface((bullet_width, 12))
            self.image.fill((0, 255, 0))  # Зеленая плазма

        self.rect = self.image.get_rect()

        if gun:
            self.rect.centerx = gun.rect.centerx
            self.rect.top = gun.rect.top

        self.y = float(self.rect.y)
        self.speed = 10 # Базовая скорость полета пули вверх

    def update(self):
        """Перемещает пулю вверх по экрану"""
        self.y -= self.speed
        self.rect.y = int(self.y)

    def draw_bullet(self):
        """Отрисовывает пулю на экране"""
        self.screen.blit(self.image, self.rect)