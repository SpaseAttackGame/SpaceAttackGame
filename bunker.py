import pygame


class BunkerBlock(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        """Один маленький блок защитной стены"""
        super().__init__()
        self.screen = screen
        self.width, self.height = 8, 8  # Размер одного кирпичика

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 3  # 3 жизни у каждого блока стены
        self.update_color()

    def update_color(self):
        """Меняет цвет блока в зависимости от оставшихся жизней"""
        if self.health == 3:
            self.image.fill((0, 200, 0))  # Зеленый (целый)
        elif self.health == 2:
            self.image.fill((200, 200, 0))  # Желтый (трещина)
        elif self.health == 1:
            self.image.fill((200, 0, 0))  # Красный (почти разрушен)


def create_bunkers(screen, bunkers_group):
    """Строит 3 больших защитных бункера перед пушкой"""
    bunkers_group.empty()
    # Точные координаты X для центров 3-х бункеров на экране шириной 500
    bunker_positions = [100, 250, 400]

    for start_x in bunker_positions:
        # Строим сетку блоков для одного бункера
        for row in range(4):
            for col in range(8):
                # Формируем красивую арку (пропускаем центральные нижние блоки)
                if row >= 2 and 2 <= col <= 5:
                    continue

                block_x = (start_x - 32) + col * 8
                block_y = 380 + row * 8  # Размещаем бункеры чуть выше пушки

                block = BunkerBlock(screen, block_x, block_y)
                bunkers_group.add(block)