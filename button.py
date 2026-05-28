import pygame.font
import pygame

class Button():
    def __init__(self, screen, msg, y_offset=0):
        """Инициализирует атрибуты кнопки"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Размеры и свойства кнопки по умолчанию
        self.width, self.height = 200, 50
        self.button_color = (0, 150, 0)      # Зеленый цвет по умолчанию
        self.text_color = (255, 255, 255)    # Белый цвет текста
        self.font = pygame.font.Font(None, 36)

        # Создание прямоугольника кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        # Смещаем кнопку по вертикали на величину y_offset
        self.rect.centery = self.screen_rect.centery + y_offset

        # Записываем текст в msg, чтобы draw_button подхватил его с самого старта
        self.msg = msg

    def draw_button(self):
        """Рисует закрашенную кнопку и текст строго по её центру"""
        # Создаем обновленный прямоугольник на случай, если ширина изменилась динамически в коде игры
        old_center = self.rect.center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = old_center

        # Рисуем ЦЕЛЬНУЮ закрашенную кнопку
        pygame.draw.rect(self.screen, self.button_color, self.rect)

        # Рисуем красивую тонкую рамку вокруг кнопки для стиля
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 1)

        # Получаем актуальный текст кнопки и рендерим его
        current_text = getattr(self, 'msg', "Кнопка")
        self.msg_image = self.font.render(current_text, True, self.text_color)

        # Выравниваем текст четко по центру прямоугольника кнопки
        msg_image_rect = self.msg_image.get_rect()
        msg_image_rect.center = self.rect.center

        # Выводим текст на экран
        self.screen.blit(self.msg_image, msg_image_rect)