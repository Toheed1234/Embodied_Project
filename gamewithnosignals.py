import pygame
import random
import csv

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10  # Grid dimensions
CELL_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game Without Signals")

# Colors
BACKGROUND = (240, 240, 240)
GRID_COLOR = (200, 200, 200)
GOAL_COLOR = (100, 200, 100)

# Grid (0 = path, 3 = goal)
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
grid[ROWS - 1][COLS - 1] = 3  # Goal

# Place bombs
NUM_BOMBS = 20
bombs = set()
while len(bombs) < NUM_BOMBS:
    bomb = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    if bomb != (0, 0) and bomb != (ROWS - 1, COLS - 1):  # Avoid placing bombs at start/goal
        bombs.add(bomb)

# Player settings
player_pos = [0, 0]

# Step counter
steps_taken = 0

# Load character sprite
character = pygame.image.load("Character.png")  # Replace this with your own sprite if needed
character = pygame.transform.scale(character, (CELL_SIZE - 10, CELL_SIZE - 10))

# Functions
def draw_grid():
    # Draw the maze grid
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BACKGROUND, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if grid[row][col] == 3:  # Goal
                pygame.draw.rect(screen, GOAL_COLOR, rect)
                font = pygame.font.Font(None, 24)
                text = font.render("Goal", True, (0, 0, 0))
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def draw_player():
    # Draw the player character sprite
    x = player_pos[1] * CELL_SIZE + 5
    y = player_pos[0] * CELL_SIZE + 5
    screen.blit(character, (x, y))

def save_steps(steps,outcome,game_type):
    with open("steps.csv", mode="a", newline="") as file:
        writer = csv.writer(file)  
        writer.writerow([steps,outcome,game_type])     # Write steps in the first column

# Main loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            row, col = player_pos
            if event.key == pygame.K_UP and row > 0:
                player_pos[0] -= 1
                steps_taken += 1
            elif event.key == pygame.K_DOWN and row < ROWS - 1:
                player_pos[0] += 1
                steps_taken += 1
            elif event.key == pygame.K_LEFT and col > 0:
                player_pos[1] -= 1
                steps_taken += 1
            elif event.key == pygame.K_RIGHT and col < COLS - 1:
                player_pos[1] += 1
                steps_taken += 1

    # Check for bombs
    if tuple(player_pos) in bombs:
        game_over = True
        save_steps(steps_taken,"Died","Without Visual Signals")
        break

    # Check for goal
    if grid[player_pos[0]][player_pos[1]] == 3:
        game_over = True
        save_steps(steps_taken,"Goal","Without Visual Signals")
        break

    # Draw everything
    draw_grid()
    draw_player()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
