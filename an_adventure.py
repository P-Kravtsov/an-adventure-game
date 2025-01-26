import sys
import pygame
import tkinter as tk

from tkinter import messagebox
from settings import Settings
from human import Human


class AnAdventure:
    """| Overall class to manage game assets and behavior |"""

    def __init__(self):
        """| Initialize the game, and create game resources |"""

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # Create a display window
        pygame.display.set_caption("An Adventure")

        self.human = Human(self)

    def run_game(self):
        """| Start the main loop for the game |"""

        while True:
            self._check_events()
            self.human.update()
            self._update_screen()
            self.clock.tick(60)  # Limit the while loop to run at 60 FPS

    def _update_screen(self):
        """| Update images on the screen, and flip to the new screen |"""

        # Redraw the screen during each pass through the
        self.screen.fill(self.settings.bg_color)
        self.human.blitme()

        pygame.display.update()  # instead of "pygame.display.flip()" | 229 | https://www.pygame.org/docs/ref/display.html#pygame.display.update |

    def _check_events(self):
        """| Respond to key presses and mouse events |"""

        # Tracking keyboard and mouse events (event is an action that the user performs - pressing a key or moving the mouse)
        for event in pygame.event.get():  # To access the events that Pygame detects
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """| Respond to key presses |"""
        if event.key == pygame.K_RIGHT:
            self.human.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.human.moving_left = True
        elif event.key == pygame.K_UP:
            self.human.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.human.moving_down = True
        elif event.key == pygame.K_q:
            self._confirm_exit()

    def _check_keyup_events(self, event):
        """| Respond to key releases |"""
        if event.key == pygame.K_RIGHT:
            self.human.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.human.moving_left = False
        elif event.key == pygame.K_UP:
            self.human.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.human.moving_down = False

    def _confirm_exit(self):
        """| Confirm exit when 'q' key is pressed |"""
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            sys.exit()
        root.destroy()


if __name__ == "__main__":
    # Make a game instance, run the game
    adventure = AnAdventure()
    adventure.run_game()
