import pygame


class Human:
    """| A class to manage the player |"""

    def __init__(self, adventure_game):
        """| Initialize the human and set its starting position |"""

        self.screen = adventure_game.screen
        self.settings = adventure_game.settings
        self.screen_rect = adventure_game.screen.get_rect()

        # Load the human image and get its rectangle
        self.image = pygame.image.load('images/human.bmp')
        self.rect = self.image.get_rect()

        # Start each new human at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flag; start with a human that's not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """| Update the human's position based on the movement flag |"""

        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """| Draw the human at its current location |"""
        self.screen.blit(self.image, self.rect)
