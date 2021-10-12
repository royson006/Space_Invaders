import pygame
import random
from pygame.sprite import Sprite

class Boss(Sprite):
    """A class to recreate a Big boss"""

    def __init__(self,ai_game):
        """Initialize the boss."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("images/boss.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.screen.get_rect().midtop[0]-int(self.rect.width/2)
        self.rect.y = 50
        # Initial direction of the boss
        self.dir_x = random.choice([-1,1])
        self.dir_y = random.choice([-1,1])
        self.life_points = 1000

        # Store the boss exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update's the boss movement"""

        self.x += self.settings.boss_speed_x * self.dir_x
        self.y += self.settings.boss_speed_y * self.dir_y
        self.rect.x = self.x
        self.rect.y = self.y
        self._change_direction()

    def _change_direction(self):
        """Change the boss direction"""
        #Change  the direction in x
        if(self.rect.x == 0):
            self.dir_x = 1
        elif(self.rect.right == self.screen.get_rect().right):
            self.dir_x = -1

        #Change  the direction in y
        if(self.rect.y == 0):
            self.dir_y = 1
        elif(self.rect.bottom == self.screen.get_rect().bottom):
            self.dir_y = -1

    def blitime(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image,self.rect)