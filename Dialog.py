import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Big complex choice")

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
    def __init__(self, x_position, y_position, width, height, label, default_color, hover_color, label_color,
                 button_font):
        self.rect = pygame.Rect(x_position, y_position, width, height)
        self.label = label
        self.default_color = default_color
        self.hover_color = hover_color
        self.label_color = label_color
        self.font = button_font  # Updated to remove shadowing

    def draw(self, target_screen, cursor_position):
        """Draws the button with hover effect if needed."""
        color = self.hover_color if self.rect.collidepoint(cursor_position) else self.default_color
        pygame.draw.rect(target_screen, color, self.rect)
        text_surface = self.font.render(self.label, True, self.label_color)
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        target_screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, cursor_position, input_event):
        """Checks if the button is clicked."""
        return self.rect.collidepoint(cursor_position) and input_event.type == pygame.MOUSEBUTTONDOWN


# Function to move the "No" button
def move_no_button():
    """| Moves the 'No' button to a random position inside the screen window |"""
    while True:
        # Generate random position for the "No" button
        no_button.rect.x = random.randint(0, SCREEN_WIDTH - no_button.rect.width)
        no_button.rect.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - no_button.rect.height)

        # Check if the new position does not collide with the "Yes" button
        if not no_button.rect.colliderect(yes_button.rect):
            break


def draw_question(question_text):
    """| Displays the question centered above the buttons |"""
    text_surface = question_font.render(question_text, True, BLACK)
    text_x = (SCREEN_WIDTH - text_surface.get_width()) // 2
    text_y = 100  # Position the text far above the buttons
    screen.blit(text_surface, (text_x, text_y))


# Create buttons
yes_button = Button(150, 250, 100, 50, "Yes", GREEN, LIGHT_GREEN, BLACK, main_font)
no_button = Button(350, 250, 100, 50, "No", RED, LIGHT_RED, BLACK, main_font)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button clicks
        if yes_button.is_clicked(mouse_position, event):
            print("You clicked Yes!")

    # Check for "No" button hover to move it
    if no_button.rect.collidepoint(mouse_position):
        move_no_button()

    # Draw elements on screen
    draw_question("Are you ready to grade the project?")
    yes_button.draw(screen, mouse_position)
    no_button.draw(screen, mouse_position)

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
