# Python Maze Generator with Depth-First Search Algorithm

import pygame
from random import choice
from settings import Settings

# Initialize game settings using Settings class
game_settings = Settings()

# Access necessary settings such as screen dimensions via the Settings object
RESOLUTION = WIDTH, HEIGHT = game_settings.screen_width, game_settings.screen_height  # Game resolution
TILE = 100  # Size of each tile in the grid
cols, rows = WIDTH // TILE, HEIGHT // TILE  # Calculate the number of columns and rows in the grid based on resolution

# Initialize pygame for rendering the game window and managing events
pygame.init()

# Create a window with the specified resolution
screen = pygame.display.set_mode(RESOLUTION)

# Create a clock object to control the frame rate
clock = pygame.time.Clock()


# Class to represent a single cell in the maze
class Cell:
    def __init__(self, x, y):
        """| Initialize cell with its coordinates. Each cell starts with all walls intact and is unvisited |"""
        self.x, self.y = x, y  # Coordinates of the cell in the grid
        # Walls dictionary to define which walls are present around the cell
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False  # Flag to check if the cell has already been visited during maze generation

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(screen, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self):
        """| Draw the cell on the screen. Visited - filled black, walls - in dark orange |"""
        x, y = self.x * TILE, self.y * TILE  # Convert cell coordinates to pixels
        if self.visited:
            # Fill the cell's area with a black rectangle if visited
            pygame.draw.rect(screen, pygame.Color('black'), (x, y, TILE, TILE))

        # Draw the walls of the cell
        if self.walls["top"]:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y + TILE), (x, y), 2)


# Create a grid of cells for the maze
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]  # Flattened cell grid list
current_cell = grid_cells[0]  # Start at the first cell in the grid
stack = []  # Stack to hold the path

# Main game loop
while True:
    screen.fill(pygame.Color('darkslategray'))  # Fill the screen with the background color

    # Handle game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Draw all cells (walls and visited states) on the screen
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell() # Highlight the current cell

    # Update display
    pygame.display.flip()

    # Cap the frame rate to the specified FPS (via game settings)
    clock.tick(game_settings.fps)
