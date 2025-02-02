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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont('Arial', 40)

# Button properties
yes_button = pygame.Rect(150, 150, 100, 50)
no_button = pygame.Rect(350, 150, 100, 50)


def draw_button(rect, text, button_color, text_color):
    """| Draws a button with centered text |"""
    # Draw the button rectangle
    pygame.draw.rect(screen, button_color, rect)

    # Render the text
    text_surface = font.render(text, True, text_color)

    # Calculate the text's position to center it inside the button
    text_x = rect.x + (rect.width - text_surface.get_width()) // 2
    text_y = rect.y + (rect.height - text_surface.get_height()) // 2

    # Blit the text onto the screen
    screen.blit(text_surface, (text_x, text_y))



def move_no_button():
    """Moves the 'No' button to a random position inside the screen window."""
    no_button.x = random.randint(0, SCREEN_WIDTH - no_button.width)
    no_button.y = random.randint(0, SCREEN_HEIGHT - no_button.height)


# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Detect click on "Yes" button
            if yes_button.collidepoint(event.pos):
                print("You clicked Yes!")

    # Get mouse position and check hover over "No" button
    mouse_pos = pygame.mouse.get_pos()
    if no_button.collidepoint(mouse_pos):
        move_no_button()

    # Draw buttons with centered text
    draw_button(yes_button, "Yes", GREEN, BLACK)
    draw_button(no_button, "No", RED, BLACK)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()