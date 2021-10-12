import pygame.font
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """This is a class for the managment of alien bullet's"""

    def __init__(self, ai_game,location):
        super().__init__()
        self.ai = ai_game
        self.settings = ai_game.settings
        self.x = location["x"]
        self.y = location["y"]

        # Store the bullet's position as a decimal value.
        # self.y = float(self.rect.y)
    def update(self):
        """Update the location of the bullet in the scree"""
        # Update the decimal position of the bullet.
        self.y += self.settings.alien_bullet_speed


    def draw(self):
        """Draw the bullet to the screen."""
        self.rect=pygame.draw.circle(self.ai.screen,
                                    self.settings.alien_bullet_color,
                                    (self.x ,self.y),
                                    self.settings.alien_bullet_size)

