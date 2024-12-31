class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""
        # Настройки экрана
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.fleet_drop_speed = 10
        # 1 вправо / -1 влево
        self.fleet_direction = 1
      # Темп ускорения игры
        self.speedup_scale = 1.2
        self.score_scale = 1.5

    def initialize_easy_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed = 1.0
        self.bullet_speed = 1
        self.alien_speed = 0.2
    
    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed = 1.5
        self.bullet_speed = 1
        self.alien_speed = 0.5
        self.alien_points = 50

    def initialize_hard_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed = 2.0
        self.bullet_speed = 1
        self.alien_speed = 1.0

    def increase_speed(self):
        """Увеличивает скорость игры"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points + self.score_scale)