import pygame
from pygame.sprite import Sprite

class Gun(Sprite):
    def __init__(self, screen,stats):
        """инициализация пушки"""
        super(Gun, self).__init__()
        self.screen = screen
        self.stats = stats
        self.image = pygame.image.load('original(2).png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.mright = False
        self.mleft = False
        self.center = float(self.rect.centerx)

    def output(self):
        # Рисуем саму пушку
        self.screen.blit(self.image, self.rect)

        # 🛡️ ПЕРЕНЕСЛИ СЮДА: Если щит активен, рисуем неоновое кольцо прямо вокруг пушки
        if hasattr(self.stats, 'shield') and self.stats.shield == 1:
            pygame.draw.circle(self.screen, (0, 255, 255), self.rect.center, 50, 3)

    def update_gun(self):
        """Обновляет позицию пушки с учетом прокачки лазерного пулемета"""
        speed = 12.0 * (1 + (self.stats.rapid_fire - 1) * 0.1)

        # Движение вправо и влево
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += speed
        if self.mleft and self.rect.left > 0:
            self.center -= speed

        self.rect.centerx = int(self.center)

        # ⚓ Прижимаем корабль к нижнему краю, чтобы он не летал по небу!
        self.rect.bottom = self.screen_rect.bottom

        if hasattr(self.stats, 'plasma_size'):
            pass