import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Serious difficult choice")

# Colors
WHITE = (210, 210, 210)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 220, 0)
LIGHT_GREEN = (100, 255, 100)
LIGHT_RED = (255, 100, 100)

# Fonts
main_font = pygame.font.SysFont('Arial', 40)
question_font = pygame.font.SysFont('Arial', 30)


class Button:
    """A class for buttons with hover effect and click detection."""

    def __init__(self, x_position, y_position, width, height, label,
                 default_color, hover_color, label_color, button_font):
        self.rect = pygame.Rect(x_position, y_position, width, height)
        self.label = label
        self.default_color = default_color
        self.hover_color = hover_color
        self.label_color = label_color
        self.font = button_font

    def draw(self, target_screen, cursor_position):
        """Draws the button, changing color on hover."""
        color = self.hover_color if self.rect.collidepoint(cursor_position) else self.default_color
        pygame.draw.rect(target_screen, color, self.rect)
        text_surface = self.font.render(self.label, True, self.label_color)
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        target_screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, cursor_position, input_event):
        """Checks if the button is clicked by the player."""
        return self.rect.collidepoint(cursor_position) and input_event.type == pygame.MOUSEBUTTONDOWN


class UIManager:
    """Handles rendering of UI elements like questions and messages."""

    def __init__(self):
        self.question = ""
        self.sub_message = ""

    def set_question(self, question, sub_message=""):
        """Sets the main question and optional sub-message."""
        self.question = question
        self.sub_message = sub_message

    def draw(self, window):
        """Draws the question and sub-message in the center of the top half of the screen."""
        # Draw the main question
        question_surface = question_font.render(self.question, True, BLACK)
        question_x = (SCREEN_WIDTH - question_surface.get_width()) // 2
        question_y = (SCREEN_HEIGHT // 2 - question_surface.get_height()) // 2  # Center in top half
        window.blit(question_surface, (question_x, question_y))

        # Draw sub-message below the question
        if self.sub_message:
            sub_message_surface = question_font.render(self.sub_message, True, BLACK)
            sub_message_x = (SCREEN_WIDTH - sub_message_surface.get_width()) // 2
            sub_message_y = question_y + question_surface.get_height() + 10  # Offset slightly below
            window.blit(sub_message_surface, (sub_message_x, sub_message_y))

class GameManager:
    """Manages the game state and transitions."""

    def __init__(self):
        self.state = "main"  # Default state at startup

    def handle_event(self, input_event, cursor_position, interface_manager):
        """Handles events for the current game state."""
        if self.state == "main":
            # Handle clicks in the "main" state
            if yes_button.is_clicked(cursor_position, input_event):
                self.state = "grades"
                interface_manager.set_question("What grade will you give to the project?")
            elif no_button.rect.collidepoint(cursor_position):
                move_button(no_button, [no_button, yes_button])
        elif self.state == "grades":
            # Handle clicks in the "grades" state
            for grade_button in grades:
                if grade_button.is_clicked(cursor_position, input_event):
                    interface_manager.set_question(
                        "What grade will you give to the project?",
                        "Great choice! So unexpected and pleasant ><"
                    )
                elif grade_button.rect.collidepoint(cursor_position) and grade_button.label != "5":
                    move_button(grade_button, grades)

    def draw_buttons(self, pointer_position):
        """Draws the appropriate buttons for each game state."""
        if self.state == "main":
            yes_button.draw(screen, pointer_position)
            no_button.draw(screen, pointer_position)
        elif self.state == "grades":
            for grade_button in grades:
                grade_button.draw(screen, pointer_position)


def create_button(x, y, width, height, label, is_special=False):
    """Creates and returns a Button with specified properties."""
    if is_special:
        default_color, hover_color = GREEN, LIGHT_GREEN
    else:
        default_color, hover_color = RED, LIGHT_RED
    return Button(x, y, width, height, label, default_color, hover_color, BLACK, main_font)


def move_button(button, all_buttons):
    """Moves the specified button to a random valid position."""
    while True:
        # Randomly position button within the bottom half of the screen
        button.rect.x = random.randint(0, SCREEN_WIDTH - button.rect.width)
        button.rect.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - button.rect.height)

        # Make sure the button doesn't overlap with others
        collision = False
        for other_button in all_buttons:
            if other_button is not button and button.rect.colliderect(other_button.rect):
                collision = True
                break
        if not collision:
            break


# Button setup
yes_button = create_button(150, 250, 100, 50, "Yes", is_special=True)
no_button = create_button(350, 250, 100, 50, "No", is_special=False)
grades = [
    create_button(50 + (100 * (i - 1)), SCREEN_HEIGHT // 2 + 50, 50, 50, str(i), is_special=(i == 5))
    for i in range(1, 6)
]

# Instantiate classes for UI and game management
ui_manager = UIManager()
game_manager = GameManager()

# Set initial question
ui_manager.set_question("Are you ready to grade the project?")

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game
        game_manager.handle_event(event, mouse_position, ui_manager)

    # Draw the UI elements and buttons
    ui_manager.draw(screen)
    game_manager.draw_buttons(mouse_position)

    # Update the screen
    pygame.display.flip()

# Quit pygame
pygame.quit()
