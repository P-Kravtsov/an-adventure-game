import math
import sys
import pygame

from settings import Settings
from human import Human
from enemy import Enemy


class AnAdventure:
    """| Overall class to manage game assets and behavior |"""

    def __init__(self):
        """| Initialize the game, and create game resources |"""

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) # Windowed mode
        self.settings.screen_width = self.screen.get_rect().width,
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("An Adventure")

        self.human = Human(self)
        self.enemy = Enemy(self)
        self.running = True
        self.paused = False
        self.blackjack_triggered = False  # To prevent repeated Blackjack triggering

    # Old not working code -
    # distance = self._calculate_distance(self.human, self.enemy)
    # if distance <= 35:
    #     print(f"Distance is {distance}, starting Blackjack...")  # Debugging print
    #     self._start_blackjack_game() are **outside the `while self.running` loop**, which means they are never executed as part of the game loop.
    # This happens because:
    # 1. The code to calculate the distance and trigger Blackjack is **after** the game loop exits (`while self.running:`).
    # 2. When the game runs, the `pygame.quit()` and `sys.exit()` calls terminate the program **before the distance check is even reached**.

    # def run_game(self):
    #     """| Start the main loop for the game |"""
    #
    #     while self.running:
    #         self._check_events()
    #         if not self.paused:  # Only update the game if not paused
    #             self.human.update()
    #             self.enemy.update()
    #             self._update_screen()
    #         self.clock.tick(self.settings.fps)  # Limit the loop to run at 60 FPS
    #
    #     # Check the distance between human and enemy
    #     distance = self._calculate_distance(self.human, self.enemy)
    #     if distance <= 35:
    #         print(f"Distance is {distance}, starting Blackjack...")  # Debugging print
    #         self._start_blackjack_game()

    def run_game(self):
        """| Start the main loop for the game |"""

        while self.running:
            self._check_events()

            # Pause logic ensures the game only updates if not paused
            if not self.paused:
                self.human.update()
                self.enemy.update()
                self._update_screen()

                # Check the distance between human and enemy
                distance = self._calculate_distance(self.human, self.enemy)
                print(f"Distance between human and enemy: {distance}")  # Debugging print

                # Trigger Blackjack only once
                if distance <= 35 and not self.blackjack_triggered:
                    print("Monster radius triggered! Starting Blackjack...")  # Debugging print
                    self.blackjack_triggered = True  # Mark Blackjack as triggered
                    self._start_blackjack_game()  # Start the Blackjack game
            else:
                self.show_pause_menu()  # Render pause menu if paused

            self.clock.tick(self.settings.fps)  # Maintain consistent FPS

        pygame.quit()
        sys.exit()

    def _update_screen(self):
        """| Update images on the screen, and flip to the new screen |"""

        # Redraw the screen during each pass through the
        self.screen.fill(self.settings.bg_color)
        self.human.blitme()  # Draw the player
        self.enemy.blitme()  # Draw the enemy

        if self.paused:
            font = pygame.font.Font(None, 72)
            text = font.render("Game Paused - Blackjack in Progress", True, (255, 0, 0))
            self.screen.blit(text, (self.settings.screen_width[0] // 4, self.settings.screen_height // 2))

        pygame.display.flip()  # instead of "pygame.display.update()" | 229 | https://www.pygame.org/docs/ref/display.html#pygame.display.update |

    def toggle_pause(self):
        """Toggle the pause state of the game."""
        self.paused = not self.paused

        if self.paused:
            print("The game is now paused.")
        else:
            print("The game has resumed.")

    def show_pause_menu(self):
        """| Display a pause menu |"""
        # Black out the screen
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)  # Set transparency (0 is fully transparent, 255 is solid black)
        overlay.fill((0, 0, 0))  # Black color
        self.screen.blit(overlay, (0, 0))

        # Render the "Paused" text
        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (255, 255, 255))  # White text
        self.screen.blit(text, (self.settings.screen_width // 2 - 100,
                                self.settings.screen_height // 2 - 50))
        pygame.display.flip()

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
            if event.type == pygame.QUIT:
                self.running = False

    def _check_keydown_events(self, event):
        """| Respond to key presses |"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.human.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.human.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.human.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.human.moving_down = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            self._confirm_exit()
        elif event.key == pygame.K_p:
                self.toggle_pause()

    def _check_keyup_events(self, event):
        """| Respond to key releases |"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.human.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.human.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.human.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.human.moving_down = False

    def _confirm_exit(self):
        """| Confirm exit when 'q' key is pressed |"""
        font = pygame.font.Font(None, 36)
        text = font.render("Quit? Press (Q)uit / (Y)es / (ESC)ape to leave or (N)o to stay", True, (0, 0, 0))
        print("One of escape keys pressed - escaping")
        self.screen.blit(text, (50, 50))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y or event.key == pygame.K_q or event.key == pygame.K_ESCAPE:  # Yes / Q / Esc to quit
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_n:  # No to exit confirmation
                        return

    def _calculate_distance(self, obj1, obj2):
        """| Calculate the distance between two objects |"""
        dx = obj1.rect.centerx - obj2.rect.centerx
        dy = obj1.rect.centery - obj2.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        print(f"Calculated distance: {distance}")  # Debugging print
        return distance

    def _start_blackjack_game(self):
        """| Start the Blackjack game in a new window and pause the adventure game |"""
        import subprocess

        print("Starting Blackjack...")  # Debugging print
        self.paused = True  # Pause the game while Blackjack runs

        try:
            # Ensure the path to blackjack.py is correct
            import os
            blackjack_path = os.path.join(os.path.dirname(__file__), 'blackjack.py')
            subprocess.run(["python", blackjack_path])  # Replace with the exact path if needed
        except FileNotFoundError:
            print(f"Error: blackjack.py not found at {blackjack_path}!")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

        self.paused = False  # Resume the adventure game after Blackjack ends
        self.blackjack_triggered = False  # Allow retriggering if needed
        print("Blackjack ended, resuming AnAdventure...")


if __name__ == "__main__":
    # Make a game instance, run the game
    adventure = AnAdventure()
    adventure.run_game()
