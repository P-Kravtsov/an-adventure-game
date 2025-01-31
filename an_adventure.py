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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
        self.settings.screen_width = self.screen.get_rect().width,
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("An Adventure")

        self.human = Human(self)
        self.enemy = Enemy(self)
        self.running = True

    def run_game(self):
        """| Start the main loop for the game |"""

        while self.running:
            self._check_events()
            self.human.update()
            self.enemy.update()
            self._update_screen()
            self.clock.tick(self.settings.fps)  # Limit the while loop to run at 60 FPS

            # Check the distance between human and enemy
            distance = self._calculate_distance(self.human, self.enemy)
            if distance <= 20:
                self._start_blackjack_game()

        pygame.quit()
        sys.exit()

    def _update_screen(self):
        """| Update images on the screen, and flip to the new screen |"""

        # Redraw the screen during each pass through the
        self.screen.fill(self.settings.bg_color)
        self.human.blitme() # Draw the player
        self.enemy.blitme() # Draw the enemy

        pygame.display.flip()  # instead of "pygame.display.update()" | 229 | https://www.pygame.org/docs/ref/display.html#pygame.display.update |

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
        """Calculate the distance between two objects."""
        dx = obj1.rect.centerx - obj2.rect.centerx
        dy = obj1.rect.centery - obj2.rect.centery
        return math.sqrt(dx**2 + dy**2)

    def _start_blackjack_game(self):
        """Start the Blackjack game."""
        import blackjack
        blackjack_game = blackjack.BlackjackGame()
        blackjack_game.main()

if __name__ == "__main__":
    # Make a game instance, run the game
    adventure = AnAdventure()
    adventure.run_game()
