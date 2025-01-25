import sys

import pygame


class AnAdventure:
    """| Overall class to manage game assets and behavior |"""

    def __init__(self):
        """| Initialize the game, and create game resources |"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1200, 800))  # Create a display window
        pygame.display.set_caption("An Adventure")
        self.bg_color = (234, 230, 230)

    def run_game(self):
        """| Start the main loop for the game |"""

        while True:
            # Watch for keyboard and mouse events (event is an action that the user performs - pressing a key or moving the mouse)
            for event in pygame.event.get():  # To access the events that Pygame detects
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the
            self.screen.fill(self.bg_color)

            # Make only a portion of the screen to be updated, instead of the entire area
            pygame.display.update()  # pygame.display.flip() | 229 | https://www.pygame.org/docs/ref/display.html#pygame.display.update |
            self.clock.tick(60)  # Limit the while loop to run at 60 FPS


if __name__ == "__main__":
    # Make a game instance, run the game
    an_adventure = AnAdventure()
    an_adventure.run_game()
