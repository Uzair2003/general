# GUI Connect4 using Pygame
# Uzair

import sys
import math
import numpy as np
import pygame

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (238, 0, 0)
YELLOW = (255, 255, 0)

# Board dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7

# Pygame initializations
pygame.init()
SQUARE_SIZE = 90
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
RADIUS = int(SQUARE_SIZE / 2 - 5)
FONT = pygame.font.SysFont("Verdana", 85)

# Function to initialize the game board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

# Function to place a piece on the board
def place_piece(board, row, col, piece):
    board[row][col] = piece

# Function to check if a column has space
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Function to find the next open row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Function to check for a winning move
def is_winning_move(board, piece):
    # Horizontal, Vertical, Positive Diagonal, Negative Diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all([board[r][c + i] == piece for i in range(4)]):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all([board[r + i][c] == piece for i in range(4)]):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all([board[r + i][c + i] == piece for i in range(4)]):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all([board[r - i][c + i] == piece for i in range(4)]):
                return True

# Function to draw the board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()

# Game initialization
board = create_board()
game_over = False
turn = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
draw_board(board)
pygame.display.update()

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            color = RED if turn == 0 else YELLOW
            pygame.draw.circle(screen, color, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARE_SIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                piece = 1 if turn == 0 else 2
                place_piece(board, row, col, piece)

                if is_winning_move(board, piece):
                    label = FONT.render(f"Player {piece} Wins!", 1, RED if piece == 1 else YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

            draw_board(board)
            turn = (turn + 1) % 2

            if game_over:
                pygame.time.wait(3000)