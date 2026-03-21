import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 12, 12
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minefield Crossing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (200, 200, 200)

# Player
player_pos = [0, ROWS // 2]

# Mines
NUM_MINES = 20
mines = set()

while len(mines) < NUM_MINES:
    x = random.randint(0, COLS - 1)
    y = random.randint(0, ROWS - 1)
    if [x, y] != player_pos and x != 0:
        mines.add((x, y))

# Game loop
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

win = False
lose = False

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not (win or lose):
            if event.key == pygame.K_UP:
                player_pos[1] = max(0, player_pos[1] - 1)
            elif event.key == pygame.K_DOWN:
                player_pos[1] = min(ROWS - 1, player_pos[1] + 1)
            elif event.key == pygame.K_LEFT:
                player_pos[0] = max(0, player_pos[0] - 1)
            elif event.key == pygame.K_RIGHT:
                player_pos[0] = min(COLS - 1, player_pos[0] + 1)

    # Check lose
    if tuple(player_pos) in mines:
        lose = True

    # Check win
    if player_pos[0] == COLS - 1:
        win = True

    # Draw grid
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Draw mines (hidden until lose)
    if lose:
        for (mx, my) in mines:
            rect = pygame.Rect(mx * CELL_SIZE, my * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, RED, rect)

    # Draw player
    rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, rect)

    # Draw goal column
    for row in range(ROWS):
        rect = pygame.Rect((COLS - 1) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect, 3)

    # Display messages
    if win:
        text = font.render("YOU WIN!", True, GREEN)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
    elif lose:
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
