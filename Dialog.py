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


# Function to move a button
def move_button(button, all_buttons):
    """Moves the specified button to a random position inside the bottom half of the screen."""
    while True:
        # Generate random position for the button within the bottom half of the screen
        button.rect.x = random.randint(0, SCREEN_WIDTH - button.rect.width)
        button.rect.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - button.rect.height)

        # Ensure the button does not collide with any other button
        collision = False
        for other_button in all_buttons:
            if other_button is not button and button.rect.colliderect(other_button.rect):
                collision = True
                break
        if not collision:
            break


def draw_question(question_text, sub_message="Pick any option you like"):
    """Displays the main question with an optional sub-message below it."""
    # Render the main question
    text_surface = question_font.render(question_text, True, BLACK)
    text_x = (SCREEN_WIDTH - text_surface.get_width()) // 2
    text_y = 15  # Place it near the top of the screen
    screen.blit(text_surface, (text_x, text_y))

    # Render the optional sub-message slightly below the main question
    if sub_message:
        sub_message_surface = question_font.render(sub_message, True, BLACK)
        sub_message_x = (SCREEN_WIDTH - sub_message_surface.get_width()) // 2
        sub_message_y = text_y + 50  # Place it slightly below the main question
        screen.blit(sub_message_surface, (sub_message_x, sub_message_y))


# Create buttons
yes_button = Button(150, 250, 100, 50, "Yes", GREEN, LIGHT_GREEN, BLACK, main_font)
no_button = Button(350, 250, 100, 50, "No", RED, LIGHT_RED, BLACK, main_font)

# Create grade buttons in the same row
grades = []
for i in range(1, 6):
    if i == 5:  # Grade 5 button (different color)
        default_color, hover_color = GREEN, LIGHT_GREEN
    else:  # Other grade buttons (red color)
        default_color, hover_color = RED, LIGHT_RED

    # Horizontal placement for the grades in the bottom half
    grade_button = Button(50 + (100 * (i - 1)), SCREEN_HEIGHT // 2 + 50, 50, 50, str(i), default_color, hover_color,
                          BLACK, main_font)
    grades.append(grade_button)

# State to track message
message = ""

# Application state
state = "main"  # Can be "main" or "grades"

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Get mouse position
    mouse_position = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button clicks based on state
        if state == "main":
            if yes_button.is_clicked(mouse_position, event):
                # Switch to the grades state
                state = "grades"
                message = ""  # Clear any previous message
            if no_button.rect.collidepoint(mouse_position):
                move_button(no_button, [no_button, yes_button])
        elif state == "grades":
            for grade_button in grades:
                if grade_button.is_clicked(mouse_position, event):
                    # Display message for selected grade
                    message = "Great choice! So unexpected and pleasant ><"
                elif grade_button.rect.collidepoint(mouse_position) and grade_button.label != "5":
                    # Avoid hover only for grades except 5
                    move_button(grade_button, grades)

    # Drawing based on state
    if state == "main":
        draw_question("Are you ready to grade the project?")
        yes_button.draw(screen, mouse_position)
        no_button.draw(screen, mouse_position)
    elif state == "grades":
        draw_question("What grade will you give to the project?", message)
        for grade_button in grades:
            grade_button.draw(screen, mouse_position)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
