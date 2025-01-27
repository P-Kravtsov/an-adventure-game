import pygame


class Enemy:
    """Class to manage the enemy."""

    def __init__(self, game):
        """Initialize the enemy and set its starting position."""
        self.screen = game.screen
        self.settings = game.settings

        # Load the enemy image and set its rect (position and size).
        self.image = pygame.image.load('images/enemy.bmp')
        self.rect = self.image.get_rect()

        # Start the enemy at a specific position.
        self.rect.x =  200
        self.rect.y =  200

        # Store the enemy's exact position as a float for fine-tuned movement.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update the enemy's position or behavior."""
        # Example: Slowly move the enemy downward.
        #self.y += 0.5
        self.rect.y = self.y  # Update rect based on new position.

    def blitme(self):
        """Draw the enemy at its current location."""
        self.screen.blit(self.image, self.rect)