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
        self.rect.topleft = self.screen_rect.topleft

        # Store a float for the human's exact horizontal position
        self.x = float(self.rect.x)  # | self.x = self.rect.x |
        self.y = float(self.rect.y)  # | self.y = self.rect.y |

        # Movement flags; start with a human that's not moving
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """| Update the human's position based on the movement flag |"""

        moved = False  # Add a moved flag

        # Update the human's x value, not the rect

        # Check if the character is moving to the right and hasn't reached the screen's right edge.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.human_speed_factor  # Move right by increasing x-coordinate
            moved = True  # Mark as moved
        if self.moving_left and self.rect.left > 0:  # check left and if reached the screen's left edge
            self.x -= self.settings.human_speed_factor  # Move left by decreasing x-coordinate
            moved = True  # Mark as moved
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.human_speed_factor
            moved = True  # Mark as moved
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.human_speed_factor
            moved = True  # Mark as moved

        # Update rect object from self.x
        self.rect.x = self.x
        self.rect.y = self.y

        return moved  # Return the movement flag

    def blitme(self):
        """| Draw the human at its current location |"""
        self.screen.blit(self.image, self.rect)
