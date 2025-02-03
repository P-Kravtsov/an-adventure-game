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
font = pygame.font.SysFont('Arial', 40)
question_font = pygame.font.SysFont('Arial', 30)


class Button:
    def __init__(self, x, y, width, height, text, default_color, hover_color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.default_color = default_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font

    def draw(self, screen, mouse_pos):
        """Draws the button with hover effect if needed."""
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.default_color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, mouse_pos, event):
        """Checks if the button is clicked."""
        return self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN


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


def draw_question(text):
    """| Displays the question centered above the buttons |"""
    text_surface = question_font.render(text, True, BLACK)
    text_x = (SCREEN_WIDTH - text_surface.get_width()) // 2
    text_y = 100  # Position the text far above the buttons
    screen.blit(text_surface, (text_x, text_y))


# Create buttons
yes_button = Button(150, 250, 100, 50, "Yes", GREEN, LIGHT_GREEN, BLACK, font)
no_button = Button(350, 250, 100, 50, "No", RED, LIGHT_RED, BLACK, font)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button clicks
        if yes_button.is_clicked(mouse_pos, event):
            print("You clicked Yes!")

    # Check for "No" button hover to move it
    if no_button.rect.collidepoint(mouse_pos):
        move_no_button()

    # Draw elements on screen
    draw_question("Are you ready to grade the project?")
    yes_button.draw(screen, mouse_pos)
    no_button.draw(screen, mouse_pos)

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
