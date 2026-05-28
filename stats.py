import pygame

class Stats():
    """Отслеживание статистики игры и магазина"""

    def __init__(self):
        """Инициализирует базовую статистику при запуске игры"""
        # 🌟 ПЕРЕМЕННЫЕ МАГАЗИНА (Инициализируются ОДИН РАЗ за весь запуск игры)
        self.score = 1000  # Твой стартовый бюджет

        # Уровни улучшений (сохраняются при перезапуске игры)
        self.double_shot = 1
        self.plasma_size = 1
        self.shield = 0  # Твой щит! Теперь он не обнулится кнопкой Играть
        self.rapid_fire = 1
        self.time_freeze_ammo = 0
        self.pierce_shot = 0
        self.nuke_bombs = 0
        self.cluster_bombs = 0

        # Цены на улучшения (чтобы не сбрасывались в начальные)
        self.double_shot_cost = 1500
        self.plasma_size_cost = 300
        self.shield_cost = 800
        self.rapid_fire_cost = 400
        self.time_freeze_cost = 500
        self.pierce_cost = 1000
        self.nuke_cost = 600

        # Флаги доступности оружия
        self.has_laser = 1
        self.has_plasma = 1
        self.has_railgun = 0

        # Чтение рекорда из файла
        try:
            with open("highscore.txt", "r") as f:
                content = f.readline().strip()
                self.high_score = int(content) if content else 0
        except FileNotFoundError:
            self.high_score = 0

        # Теперь вызываем сброс только боевых параметров
        self.reset_stats()
        self.run_game = False

    def reset_stats(self):
        """Сбрасывает только параметры текущего боевого заезда"""
        self.guns_left = 3  # Сброс жизней пушки

        # Дополнительные боевые модификаторы
        self.bouncing_bullets = 0
        self.nano_damage = 0
        self.spawn_mutant = 0

        # Параметры босса UFO
        self.ufo_active = False
        self.ufo_hp = 4
        self.ufo_max_hp = 4
        self.ufo_spawn_delay = 30.0

        # Режимы оружия в бою
        self.plasma_mode = "ready"
        self.plasma_timer_start = 0.0
        self.current_weapon = "plasma"
        self.game_paused = False