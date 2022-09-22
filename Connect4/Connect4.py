# GUI Connect4 using Pygame
# Uzair

import sys
import math
import numpy as np
import pygame

# Blue board and Black background
blue = (0,0,255)
black = (0,0,0)
# Red and Yellow for both players
red = (238,0,0)
yellow = (255,255,0)

row_count = 6
column_count = 7

# Initialize the board usign the 6x7 layout 
def create_board():
	board = np.zeros((row_count,column_count))
	return board

def place_piece(board, row, col, piece):
	board[row][col] = piece

# Check if the spot where the peice is being dropped is empty
def valid_location(board, col):
	return board[row_count-1][col] == 0

def get_next_open_row(board, col):
	for row in range(row_count):
		if board[row][col] == 0:
			return row

def display_board(board):
	print(np.flip(board, 0))

# Check if the conditions needed to win are met by either player
def winning_move(board, piece):
	# Check the horizontal axis for a win
	for col in range(column_count-3):
		for row in range(row_count):
			if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
				return True

	# Check the vertical axis for a win
	for col in range(column_count):
		for row in range(row_count-3):
			if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
				return True

	# Check for a upward sloping diagonal win
	for col in range(column_count-3):
		for row in range(row_count-3):
			if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
				return True

	# Check for a downward sloping diagonal win
	for col in range(column_count-3):
		for row in range(3, row_count):
			if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
				return True

def draw_board(board):
	for col in range(column_count):
		for row in range(row_count):
			pygame.draw.rect(screen, blue, (col*square_size, row*square_size + square_size, square_size, square_size))
			pygame.draw.circle(screen, black, (int(col*square_size + square_size/2), int(row*square_size + square_size + square_size/2)), radius)
	
	for col in range(column_count):
		for row in range(row_count):		
			if board[row][col] == 1:
				pygame.draw.circle(screen, red, (int(col*square_size + square_size/2), height-int(row*square_size + square_size/2)), radius)
			elif board[row][col] == 2: 
				pygame.draw.circle(screen, yellow, (int(col*square_size + square_size/2), height-int(row*square_size + square_size/2)), radius)
	pygame.display.update()


board = create_board()
display_board(board)
game_over = False
turn = 0

pygame.init()

# Defining boundaries for the game area 
square_size = 90
width = column_count * square_size
height = (row_count + 1) * square_size
size = (width, height)
radius = int(square_size/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("Verdana", 85)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, black, (0,0, width, square_size))
			posx = event.pos[0]
			# Show a red circle on Player 1's turn
			if turn == 0:
				pygame.draw.circle(screen, red, (posx, int(square_size/2)), radius)
			# Show a yellow circle on Player 2's turn
			else: 
				pygame.draw.circle(screen, yellow, (posx, int(square_size/2)), radius)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, black, (0,0, width, square_size))
			# Ask for Player 1's Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/square_size))

				if valid_location(board, col):
					row = get_next_open_row(board, col)
					place_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render("Player 1 Wins!", 1, red)
						screen.blit(label, (1,1))
						game_over = True


			# Ask for Player 2's Input
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/square_size))

				if valid_location(board, col):
					row = get_next_open_row(board, col)
					place_piece(board, row, col, 2)

					if winning_move(board, 2):
						label = myfont.render("Player 2 Wins!", 1, yellow)
						screen.blit(label, (1,1))
						game_over = True

			display_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)
