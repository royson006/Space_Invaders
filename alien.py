import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""


    def __init__(self, ai_game,level = 1):
        """Initialize the alien and set its starting position."""
        self.alien_types = {"level_1":{"health":100,
                                        "img":"images/alien.bmp"},
                            "level_2":{"health":300,
                                        "img":"images/alien_level2.bmp"},
                            "level_3":{"health":500,
                                        "img":"images/alien_level3.bmp"},
                            }

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.health = self.alien_types["level_"+str(level)]["health"]
        self.image = self.alien_types["level_"+str(level)]["img"]


        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(self.image)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if(self.rect.right >= screen_rect.right or self.rect.left  <= 0):
            return True


    def update(self):
        """Move alien to the right"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x =self.x
