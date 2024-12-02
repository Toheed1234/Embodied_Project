import pygame
import random
import csv
import tkinter as tk

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10  # Grid dimensions
CELL_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH + 100, HEIGHT + 100))  # Extra space for signals
pygame.display.set_caption("Maze Game with Signals")

# Colors
BACKGROUND = (240, 240, 240)
GRID_COLOR = (200, 200, 200)
GOAL_COLOR = (100, 200, 100)
BOMB_COLOR = (200, 100, 100)
SIGNAL_GREEN = (50, 205, 50)
SIGNAL_YELLOW = (255, 215, 0)
SIGNAL_RED = (255, 69, 0)

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
            rect = pygame.Rect(col * CELL_SIZE + 50, row * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BACKGROUND, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            if grid[row][col] == 3:  # Goal
                pygame.draw.rect(screen, GOAL_COLOR, rect)
                font = pygame.font.Font(None, 24)
                text = font.render("Goal", True, (0, 0, 0))
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2 + 50, row * CELL_SIZE + 50 + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    # Draw the boundary
    pygame.draw.rect(screen, (0, 0, 0), (50, 50, WIDTH, HEIGHT), 5)

def draw_player():
    # Draw the player character sprite
    x = player_pos[1] * CELL_SIZE + 55
    y = player_pos[0] * CELL_SIZE + 55
    screen.blit(character, (x, y))

def calculate_signals():
    signals = {'top': SIGNAL_GREEN, 'bottom': SIGNAL_GREEN, 'left': SIGNAL_GREEN, 'right': SIGNAL_GREEN}
    row, col = player_pos

    for bomb_row, bomb_col in bombs:
        if bomb_row == row and bomb_col > col:  # Bomb to the right
            distance = bomb_col - col
            signals['right'] = SIGNAL_RED if distance == 1 else (SIGNAL_YELLOW if distance == 2 else signals['right'])
        elif bomb_row == row and bomb_col < col:  # Bomb to the left
            distance = col - bomb_col
            signals['left'] = SIGNAL_RED if distance == 1 else (SIGNAL_YELLOW if distance == 2 else signals['left'])
        elif bomb_col == col and bomb_row > row:  # Bomb below
            distance = bomb_row - row
            signals['bottom'] = SIGNAL_RED if distance == 1 else (SIGNAL_YELLOW if distance == 2 else signals['bottom'])
        elif bomb_col == col and bomb_row < row:  # Bomb above
            distance = row - bomb_row
            signals['top'] = SIGNAL_RED if distance == 1 else (SIGNAL_YELLOW if distance == 2 else signals['top'])

    return signals

def draw_signals(signals):
    # Draw directional signals outside the boundary
    pygame.draw.circle(screen, signals['top'], (WIDTH // 2 + 50, 25), 20)  # Top
    pygame.draw.circle(screen, signals['bottom'], (WIDTH // 2 + 50, HEIGHT + 75), 20)  # Bottom
    pygame.draw.circle(screen, signals['left'], (25, HEIGHT // 2 + 50), 20)  # Left
    pygame.draw.circle(screen, signals['right'], (WIDTH + 75, HEIGHT // 2 + 50), 20)  # Right

def open_feedback_window(outcome):
    def submit_feedback(answer):
        save_feedback(answer,outcome,"With Visual Signals")
        feedback_window.destroy()
        pygame.quit()

    feedback_window = tk.Tk()
    feedback_window.title("Feedback")
    feedback_window.geometry("300x150")
    feedback_window.resizable(False, False)

    # Center-aligned content
    label = tk.Label(feedback_window, text=f"Did the signals help?\n({outcome})", font=("Arial", 14), anchor="center", justify="center")
    label.pack(pady=20)

    # Create a frame for buttons
    button_frame = tk.Frame(feedback_window)
    button_frame.pack(pady=10)

    # Add buttons
    yes_button = tk.Button(button_frame, text="Yes", width=10, command=lambda: submit_feedback("Yes"))
    yes_button.grid(row=0, column=0, padx=10)

    no_button = tk.Button(button_frame, text="No", width=10, command=lambda: submit_feedback("No"))
    no_button.grid(row=0, column=1, padx=10)

    feedback_window.mainloop()

def save_feedback(value,outcome,game_type):
    with open("feedback.csv", mode="a", newline='') as file:  # Ensure the path is accessible
        writer = csv.writer(file)
        writer.writerow([steps_taken,outcome,value,game_type])

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
        open_feedback_window("Died")
        break

    # Check for goal
    if grid[player_pos[0]][player_pos[1]] == 3:
        game_over = True
        open_feedback_window("Goal")
        break

    # Draw everything
    draw_grid()
    draw_player()

    # Update and draw signals
    signals = calculate_signals()
    draw_signals(signals)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()