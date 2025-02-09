from typing import Optional, Any
from pygame.surface import Surface
from pygame import Rect
import pygame


class Enemy:
    """| Class to manage enemies |"""

    def __init__(self, game, x: int = 500, y: int = 300, image_path: str = 'images/enemy.bmp') -> None:
        """
        Initialize the enemy and set its starting position.
        :param game: Instance of AnAdventure, providing settings and screen attributes.
        """
        self.screen: Optional[Surface] = game.screen # Allowing for the possibility that screen might be None.
        self.settings: Optional[Any] = game.settings # Allowing settings to be of any type and potentially None.

        self.image: Surface = self._load_image(image_path)

        # Set its rectangular position and size.
        self.rect: Rect = self.image.get_rect()  #The rectangle for positioning.
        self.rect.x = x
        self.rect.y = y

        # Store the position as floats for fine-tuned movement.
        self.x: float = float(self.rect.x)
        self.y: float = float(self.rect.y)

    def _load_image(self, image_path: str) -> Surface:
        """| Load the specified enemy image (default: 'enemy.bmp') |"""
        try:
            return pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Error loading enemy image at {image_path}: {e}")
            raise

    def update(self) -> None:
        """| Update the enemy's position or behavior (if any) |"""

        # This is for a simple vertical movement example, expand as needed.
        self.rect.y = int(self.y)  # Sync rectangle with position.

    def blitme(self) -> None:
        """| Draw the enemy’s image at its current location (using its Rect) |"""
        self.screen.blit(self.image, self.rect)
