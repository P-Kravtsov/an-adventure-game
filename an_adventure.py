import math
import sys
import pygame

from settings import Settings
from human import Human
from enemy import Enemy


class AnAdventure:
    """| Overall class to manage game assets and behavior |"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # Windowed mode
        pygame.display.set_caption("An Adventure")

        # Create main game objects
        self.human = Human(self)

        # First enemy at default location.
        self.enemy = Enemy(self)

        # Adjust enemy position to be precisely in the bottom-right corner
        enemy_image_path = 'images/enemy2.bmp'  # Path to the enemy image
        temp_enemy = Enemy(self, image_path=enemy_image_path)  # Temporarily load to get rect dimensions
        enemy_x = self.settings.screen_width - temp_enemy.rect.width
        enemy_y = self.settings.screen_height - temp_enemy.rect.height
        self.second_enemy = Enemy(self, x=enemy_x, y=enemy_y, image_path=enemy_image_path)

        self.running = True
        self.paused = False
        self.blackjack_triggered = False

    def _update_screen(self):
        """Update all images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        # Draw game entities.
        self.human.blitme()  # Draw the player
        if self.enemy:  # First enemy
            self.enemy.blitme()
        if self.second_enemy:  # Second enemy
            self.second_enemy.blitme()

        pygame.display.flip()

    def run_game(self):
        """| Start the main loop for the game |"""
        # Show the start screen
        self.show_start_screen()

        while self.running:
            self._check_events()

            if not self.paused:
                # Normal game logic
                player_moved = self.human.update()  # Check if human moved

                if self.human:
                    player_moved = self.human.update()  # Ensure self.human is not None

                if self.enemy is not None and player_moved:  # Only calculate if the player moved
                    self.enemy.update()
                    distance = self._calculate_distance(self.human, self.enemy)

                    # Trigger monster battle
                    if distance <= 35 and not self.blackjack_triggered:
                        print("Monster radius triggered! Game Paused, Starting Blackjack...")
                        self.blackjack_triggered = True

                        # Pause the game and show the pause screen immediately
                        self.paused = True  # Manually pause
                        self.show_pause_menu()  # Display the pause menu
                        pygame.time.delay(500)  # Optional small delay for user feedback (0.5s)

                        # Start the Blackjack game
                        self._start_blackjack_game()

                        # After returning from Blackjack, remove the monster
                        self.enemy = None  # Remove monster
                        self.paused = False  # Automatically resume the game

                # Add logic for the second enemy
                if self.second_enemy is not None and player_moved:
                    distance_to_second_enemy = self._calculate_distance(self.human, self.second_enemy)

                    if distance_to_second_enemy <= 35:  # Adjust the radius as needed
                        print("Second enemy detected! Pausing game and starting dialog...")
                        self.paused = True  # Manually pause the game
                        self.show_pause_menu()
                        pygame.time.delay(500)

                        # Launch Dialog.py
                        self._start_dialog()

                        # self.second_enemy = None  # Remove second enemy after the dialog ends
                        self.paused = False

                self._update_screen()

            else:
                self.show_pause_menu()  # Show the updated pause menu while paused

            self.clock.tick(self.settings.fps)  # Maintain consistent FPS

        pygame.quit()
        sys.exit()

    def show_start_screen(self):
        """| Display the start screen with game rules and instructions to start |"""
        self.screen.fill(self.settings.bg_color)  # Fill background with the color from settings

        # Title Display
        font_title = pygame.font.Font(None, 74)  # Large font for title
        title_text = font_title.render("An Adventure", True, (0, 0, 0))
        title_x = (self.settings.screen_width - title_text.get_width()) // 2
        title_y = 50  # Position at the top
        self.screen.blit(title_text, (title_x, title_y))

        # Rules/Instructions
        font_rules = pygame.font.Font(None, 36)  # Medium font for rules
        rules = [
            "Rules:",
            "1. Goal - to deal with Pavel and leave.",
            "2. Move using arrow keys or WASD.",
            "3. Press 'P' to pause the game.",
            "4. Press 'Q' to quit at any time."
        ]
        y_offset = 150
        for line in rules:
            rule_text = font_rules.render(line, True, (0, 0, 0))  # Black text
            rule_x = (self.settings.screen_width - rule_text.get_width()) // 2
            self.screen.blit(rule_text, (rule_x, y_offset))
            y_offset += 40  # Spacing between rules

        # Start Instructions
        font_start = pygame.font.Font(None, 48)  # Slightly larger font for start message
        start_text = font_start.render("Press any key to start the game", True, (0, 100, 20))  # Yellow
        start_x = (self.settings.screen_width - start_text.get_width()) // 2
        start_y = self.settings.screen_height - 100
        self.screen.blit(start_text, (start_x, start_y))

        # Update display
        pygame.display.flip()

        # Wait for user input on the start screen
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # Any key pressed
                    waiting = False

    def toggle_pause(self):
        """Toggle the pause state of the game."""
        self.paused = not self.paused

        if self.paused:
            print("The game is now paused.")
        else:
            print("The game has resumed.")

    def show_pause_menu(self):
        """| Display a pause menu |"""

        # Redraw the existing game screen (to ensure the game state shows correctly even when paused)
        self.screen.fill(self.settings.bg_color)  # Refill the screen with the background color
        self.human.blitme()  # Draw the player
        if self.enemy:  # Draw the monster if it still exists
            self.enemy.blitme()

        # Add a transparent dim overlay over the screen
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)  # Transparency level (0=fully transparent, 255=opaque)
        overlay.fill((0, 0, 0))  # Black overlay
        self.screen.blit(overlay, (0, 0))

        # Render the "Paused" text at the center of the screen
        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (255, 255, 255))  # White text

        # Center the paused text in the middle of the screen
        pause_x = (self.settings.screen_width - text.get_width()) // 2
        pause_y = (self.settings.screen_height - text.get_height()) // 2
        self.screen.blit(text, (pause_x, pause_y))

        # Update the display to show the paused menu
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
        distance = int(round(distance))
        #print(f"Calculated distance: {distance}")  # Debugging print
        return distance

    def _start_blackjack_game(self):
        """| Start the Blackjack game in a new window and pause the adventure game |"""
        import subprocess
        import os

        print("Starting Blackjack...")  # Debugging print
        self.paused = True  # Pause the game while Blackjack runs

        # Define blackjack_path outside try block
        blackjack_path = os.path.join(os.path.dirname(__file__), 'blackjack.py')

        # Check if the blackjack.py file exists
        if not os.path.exists(blackjack_path):
            print(f"Error: blackjack.py not found at {blackjack_path}. Please ensure the file exists.")
            return  # Exit the method early if path is invalid

        try:
            subprocess.run(["python", blackjack_path])  # Execute the Blackjack game
        except FileNotFoundError:
            print(f"Error: blackjack.py not found at {blackjack_path}!")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

    def _start_dialog(self):
        """Start the Dialog game in a new window and pause the adventure game."""
        import subprocess
        import os

        print("Launching dialog...")  # Debugging print
        self.paused = True  # Pause the game while the dialog runs

        try:
            # Dialog logic
            dialog_path = os.path.join(os.path.dirname(__file__), 'Dialog.py')
            if not os.path.exists(dialog_path):
                print(f"Error: Dialog.py not found at {dialog_path}. Please ensure the file exists.")
                return
            subprocess.run(["python", dialog_path])  # Launch Dialog.py
        except FileNotFoundError:
            print("Dialog.py file not found or path is incorrect!")
        except Exception as e:
            print(f"An unexpected error occurred when starting Dialog: {e}")

if __name__ == "__main__":
    # Make a game instance, run the game
    adventure = AnAdventure()
    adventure.run_game()
