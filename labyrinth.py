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
        """
        Initialize the cell with its coordinates and default properties.
        Each cell starts with all walls intact and is unvisited.
        """
        self.x, self.y = x, y  # Coordinates of the cell in the grid
        # Walls dictionary to define which walls are present around the cell
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False  # Flag to check if the cell has already been visited during maze generation

    def draw(self):
        """
        Draw the cell on the screen.
        Visited cells are filled with black, and walls are drawn in dark orange.
        """
        x, y = self.x * TILE, self.y * TILE  # Convert cell coordinates to pixels
        if self.visited:
            # Fill the cell's area with a black rectangle if visited
            pygame.draw.rect(screen, pygame.Color('black'), (x, y, TILE, TILE))

        # Draw the walls of the cell
        if self.walls["top"]:  # Top wall
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
        if self.walls["right"]:  # Right wall
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls["bottom"]:  # Bottom wall
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls["left"]:  # Left wall
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y + TILE), (x, y), 2)


# Create a grid of cells for the maze
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]  # Flattened cell grid list
current_cell = grid_cells[0]  # Start at the first cell in the grid
stack = []  # Stack to hold the path (used during the backtracking process)

# Main game loop
while True:
    screen.fill(pygame.Color('darkslategray'))  # Fill the screen with the background color

    # Handle game events such as quitting the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the quit event occurs, exit the game
            exit()

    # Draw all cells (walls and visited states) on the screen
    [cell.draw() for cell in grid_cells]

    # Update the display with the latest graphics
    pygame.display.flip()

    # Cap the frame rate to the specified FPS (via game settings)
    clock.tick(game_settings.fps)
