import pygame


class Enemy:
    """Class to manage enemies."""

    def __init__(self, game, x=500, y=300, image_path='images/enemy.bmp'):
        """Initialize the enemy and set its starting position."""
        self.screen = game.screen
        self.settings = game.settings

        self.image = self._load_image(image_path)

        # Set its rectangular position and size.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Store the position as floats for fine-tuned movement.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def _load_image(self, image_path):
        """| Load the specified enemy image (default: 'enemy.bmp') |"""
        try:
            return pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Error loading enemy image at {image_path}: {e}")
            raise

    def update(self):
        """Update the enemy's position or behavior (if any)."""
        # This is for a simple vertical movement example, expand as needed.
        self.rect.y = int(self.y)  # Sync rectangle with position.

    def blitme(self):
        """Draw the enemy at its current location."""
        self.screen.blit(self.image, self.rect)
