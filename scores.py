import pygame.font
from  gun import Gun
from pygame.sprite import Group
class Scores():
    """вывод игровой информации"""
    def __init__(self, screen, stats):
        """инициализируем подсчёт очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (139, 195, 74)
        self.font = pygame.font.SysFont(None, 36)
        self.image_score()
        self.image_guns()

    def image_score(self):
        """Превращает текущий счёт в графическое изображение"""
        # Форматируем число (добавляем красивые запятые или пробелы в цифры)
        score_str = f"{self.stats.score:,}"

        # Создаем белую надпись с очками на черном фоне (замените цвета на ваши, если нужно)
        self.score_image = self.font.render(score_str, True, (255, 255, 255), (0, 0, 0))
        self.score_rect = self.score_image.get_rect()

        # Размещаем счёт в верхнем правом углу экрана с отступом в 20 пикселей
        self.score_rect.right = self.screen.get_rect().right - 20
        self.score_rect.top = 20

    def image_guns(self):
        """Создает маленькие пушки для отображения оставшихся жизней"""
        self.guns = pygame.sprite.Group()
        for gun_number in range(self.stats.guns_left):
            # Создаем пушку игрока
            gun = Gun(self.screen, self.stats)

            # Принудительно загружаем в неё картинку пушки-пирамидки
            gun.image = pygame.image.load('original(2).png')

            # Масштабируем её, чтобы она была аккуратной в углу
            gun.image = pygame.transform.scale(gun.image, (20, 20))
            gun.rect = gun.image.get_rect()

            # Выстраиваем в ряд с красивым отступом
            gun.rect.x = 10 + gun_number * (gun.rect.width + 10)
            gun.rect.y = 10
            self.guns.add(gun)

    def image_high_score(self):
        """преоброзует рекорд  графическое изображение"""
        self.high_score_image = self.font.render(str(self.stats.high_score), True, self.text_color, (0, 0, 0))
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def show_score(self):
        """Выводит текущий счёт, рекорд и жизни на экран"""
        # 🔥 Проверяем: если текущий счёт побил рекорд — обновляем его!
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.image_high_score()  # Перерисовываем картинку рекорда

            # Сохраняем новый рекорд в файл, чтобы он не стёрся при перезапуске
            with open("highscore.txt", "w") as f:
                f.write(str(self.stats.high_score))

        # Отрисовываем счёт и рекорд на экране Pygame
        self.screen.blit(self.score_image, self.score_rect)
        if hasattr(self, 'high_score_image'):
            self.screen.blit(self.high_score_image, self.high_score_rect)

        # Рисуем пушечки-жизни в левом углу
        self.guns.draw(self.screen)


