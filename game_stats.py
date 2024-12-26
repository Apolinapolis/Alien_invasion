class GameStats():
    """Отслеживание статистики"""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра начинается в неактивном режиме
        self.game_active = False

    def reset_stats(self):
        """Сбросить статистику"""
        self.ships_left = self.settings.ship_limit