from random import choice, randint

import pygame

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

# Initial speed
INITIAL_FPS = 10

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, position=None, body_color=None):
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
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


class Poison(GameObject):
    def __init__(self):
        super().__init__(body_color=POISON_COLOR)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
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


class Rock(GameObject):
    def __init__(self):
        super().__init__(body_color=ROCK_COLOR)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
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


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        return self.positions[0]

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        # Check for self-collision only if the snake is long enough
        if len(self.positions) >= 3 and new_head in self.positions[2:]:
            self.reset()
            return

        # Add new head position
        self.positions.insert(0, new_head)

        # Trim positions to match the current length
        self.positions = self.positions[:self.length]

        # Update the last position for erasing the tail
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake, fps):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pygame.K_q and fps > 5:
                fps -= 1
            elif event.key == pygame.K_w and fps < 20:
                fps += 1
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
    return fps


def main():
    pygame.init()
    snake = Snake()
    apples = [Apple() for _ in range(3)]
    poison = Poison()
    rocks = [Rock() for _ in range(2)]
    fps = INITIAL_FPS

    while True:
        clock.tick(fps)
        fps = handle_keys(snake, fps)
        snake.update_direction()
        snake.move()

        occupied_positions = set(snake.positions)
        for apple in apples:
            occupied_positions.add(apple.position)
        occupied_positions.add(poison.position)
        for rock in rocks:
            occupied_positions.add(rock.position)

        if snake.get_head_position() in [rock.position for rock in rocks]:
            snake.reset()
            fps = INITIAL_FPS

        if snake.get_head_position() == poison.position:
            snake.length = max(1, snake.length - 1)
            poison.randomize_position(occupied_positions)

        for apple in apples:
            if snake.get_head_position() == apple.position:
                snake.length += 1
                apple.randomize_position(occupied_positions)

        pygame.display.set_caption(f"Snake - Length: {snake.length} - Speed: {fps}")

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        for apple in apples:
            apple.draw()
        poison.draw()
        for rock in rocks:
            rock.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
