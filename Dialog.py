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

# Button properties (moved to the bottom half of the screen)
yes_button = pygame.Rect(150, 250, 100, 50)
no_button = pygame.Rect(350, 250, 100, 50)


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
    """| Moves the 'No' button to a random position inside the screen window |"""
    while True:
        # Generate random position for the "No" button
        no_button.x = random.randint(0, SCREEN_WIDTH - no_button.width)
        no_button.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - no_button.height)

        # Check if the new position does not collide with the "Yes" button
        if not no_button.colliderect(yes_button):
            break


def draw_question(text):
    """| Displays the question centered above the buttons |"""
    text_surface = question_font.render(text, True, BLACK)

    # Center the text horizontally at the top of the screen
    text_x = (SCREEN_WIDTH - text_surface.get_width()) // 2
    text_y = 100  # Position the text far above the buttons
    screen.blit(text_surface, (text_x, text_y))


# Main loop with hover effect
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

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Hover effects for buttons
    yes_button_color = LIGHT_GREEN if yes_button.collidepoint(mouse_pos) else GREEN
    no_button_color = LIGHT_RED if no_button.collidepoint(mouse_pos) else RED

    # Check if mouse is hovering over the "No" button
    if no_button.collidepoint(mouse_pos):
        move_no_button()

    # Draw the question above the buttons
    draw_question("Are you ready to grade the project?")

    # Draw buttons with hover effect
    draw_button(yes_button, "Yes", yes_button_color, BLACK)
    draw_button(no_button, "No", no_button_color, BLACK)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()

