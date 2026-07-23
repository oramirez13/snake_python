#!/usr/bin/env python3
"""
Snake Game - A classic snake game built with pygame.

Controls:
    Arrow keys or WASD to move
    ESC to quit
    SPACE or ENTER to restart after game over

Author: Orami
"""

import pygame
import random
import sys

# ============================================================
# CONSTANTS
# ============================================================

# Window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Snake Game"
FPS = 10

# Grid
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 50, 50)
GRAY = (40, 40, 40)
YELLOW = (255, 215, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# ============================================================
# SNAKE CLASS
# ============================================================

class Snake:
    """Snake entity controlled by the player."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset snake to initial state."""
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.body = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = RIGHT
        self.grow = False

    def change_direction(self, new_direction):
        """Change direction preventing 180-degree turns."""
        # Prevent reversing direction
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def move(self):
        """Move the snake one step in current direction."""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        self.body.insert(0, new_head)

        if self.grow:
            self.grow = False
        else:
            self.body.pop()

    def check_collision(self):
        """Check if snake hits wall or itself."""
        head = self.body[0]

        # Wall collision
        if head[0] < 0 or head[0] >= GRID_WIDTH:
            return True
        if head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True

        # Self collision (skip head)
        if head in self.body[1:]:
            return True

        return False

    def eat(self):
        """Mark snake to grow on next move."""
        self.grow = True

    def draw(self, surface):
        """Draw the snake on the surface."""
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if i == 0:
                # Head - brighter green
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 1)
            else:
                # Body - slightly darker
                pygame.draw.rect(surface, DARK_GREEN, rect)
                pygame.draw.rect(surface, GREEN, rect, 1)


# ============================================================
# FOOD CLASS
# ============================================================

class Food:
    """Food item that the snake collects."""

    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self, snake_body=None):
        """Spawn food at a random position not occupied by the snake."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.position = (x, y)
            if snake_body is None or self.position not in snake_body:
                break

    def draw(self, surface):
        """Draw the food on the surface."""
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


# ============================================================
# GAME CLASS
# ============================================================

class Game:
    """Main game controller."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.SysFont("Liberation Sans", 48, bold=True)
        self.font_medium = pygame.font.SysFont("Liberation Sans", 28)
        self.font_small = pygame.font.SysFont("Liberation Sans", 20)

        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake.body)

        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.running = True

    def handle_events(self):
        """Process all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return

                if self.game_over:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.restart()
                    return

                # Direction changes
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.snake.change_direction(UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.snake.change_direction(DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.snake.change_direction(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.snake.change_direction(RIGHT)

    def update(self):
        """Update game state."""
        if self.game_over:
            return

        self.snake.move()

        # Check food collision
        if self.snake.body[0] == self.food.position:
            self.snake.eat()
            self.score += 10
            self.food.spawn(self.snake.body)

        # Check game over
        if self.snake.check_collision():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score

    def draw_grid(self):
        """Draw background grid."""
        self.screen.fill(BLACK)
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_score(self):
        """Draw score and high score at the top."""
        score_text = self.font_small.render(
            f"Score: {self.score}", True, WHITE
        )
        high_text = self.font_small.render(
            f"High Score: {self.high_score}", True, YELLOW
        )
        self.screen.blit(score_text, (10, 5))
        self.screen.blit(high_text, (WINDOW_WIDTH - high_text.get_width() - 10, 5))

    def draw_game_over(self):
        """Draw game over screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        go_text = self.font_large.render("GAME OVER", True, RED)
        go_rect = go_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )
        self.screen.blit(go_text, go_rect)

        # Final score
        score_text = self.font_medium.render(
            f"Score: {self.score}", True, WHITE
        )
        score_rect = score_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)
        )
        self.screen.blit(score_text, score_rect)

        # Restart instruction
        restart_text = self.font_small.render(
            "Press SPACE or ENTER to restart", True, GRAY
        )
        restart_rect = restart_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
        )
        self.screen.blit(restart_text, restart_rect)

    def restart(self):
        """Restart the game."""
        self.snake.reset()
        self.food.spawn(self.snake.body)
        self.score = 0
        self.game_over = False

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()

            self.draw_grid()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.draw_score()

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    game = Game()
    game.run()
