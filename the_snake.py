"""Snake game implementation with Pygame."""

import pygame
from random import randint

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
POISON_COLOR = (128, 0, 128)
ROCK_COLOR = (128, 128, 128)
SNAKE_COLOR = (0, 255, 0)

INITIAL_FPS = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class GameObject:
    """Base class for all game objects."""

    def __init__(self, position=None, body_color=None):
        """
        Initialize the game object.

        Args:
            position (tuple): The (x, y) position of the object.
            body_color (tuple): The RGB color of the object.
        """
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draw the game object."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Apple class representing food for the snake."""

    def __init__(self):
        """Initialize the apple object."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
        """
        Randomize the apple's position.

        Args:
            occupied_positions (set): Positions that are already occupied.
        """
        if occupied_positions is None:
            occupied_positions = set()
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break
