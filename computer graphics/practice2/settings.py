# settings.py

class Settings:
    def __init__(self):
        # Параметры экрана
        self.screen_width = 640
        self.screen_height = 640
        self.bg_color = (0, 0, 0)

        # Параметры корабля
        self.ship_speed = 0.5

        # Параметры снарядов
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        # Параметры инопланетян
        self.alien_speed = 10
        self.fleet_drop_speed = 3
        self.fleet_direction = 1

        # Параметры увеличения сложности
        self.speedup_scale = 1.1
        self.level = 1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Настройки, которые изменяются в ходе игры"""
        self.alien_speed = 1
        self.fleet_drop_speed = 5
        self.bullet_speed = 1.0

    def increase_speed(self):
        """Увеличение сложности игры"""
        self.alien_speed *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bullets_allowed += 1
        self.level += 1
