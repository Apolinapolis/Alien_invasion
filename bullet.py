import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        """Создание снаряда в позиции (0,0) и назначение верной позиции"""
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        """Позиция снаряда хранится в вещественном формате"""
        self.y = float(self.rect.y)

    def update(self):
        """Переместить снаряд вверх по экрану."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывести снаряд на экран."""
        pygame.draw.rect(self.screen, self.color, self.rect)