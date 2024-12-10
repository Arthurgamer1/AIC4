import numpy as np
import pygame
import sys
import math

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = -1
WINDOW_LENGTH = 4

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Dimensions
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)
clock = pygame.time.Clock()

# Game functions
def create_board():
    return np.full((ROW_COUNT, COLUMN_COUNT), EMPTY)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r

def winning_move(board, piece):
    # Horizontal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True
    # Positive diagonal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    # Negative diagonal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    return False

def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def is_terminal_node(board):
    return winning_move(board, PLAYER) or winning_move(board, AI) or not get_valid_locations(board)

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# Monte Carlo AI
class MonteCarloAI:
    def __init__(self, simulations=100):
        self.simulations = simulations

    def simulate_game(self, board, col, player):
        simulated_board = board.copy()
        row = get_next_open_row(simulated_board, col)
        drop_piece(simulated_board, row, col, player)
        current_player = 3 - player
        while not is_terminal_node(simulated_board):
            valid_moves = get_valid_locations(simulated_board)
            if not valid_moves:
                break
            random_col = np.random.choice(valid_moves)
            row = get_next_open_row(simulated_board, random_col)
            drop_piece(simulated_board, row, random_col, current_player)
            current_player = 3 - current_player
        if winning_move(simulated_board, player):
            return 1
        elif winning_move(simulated_board, 3 - player):
            return -1
        return 0

    def best_move(self, board, player):
        valid_moves = get_valid_locations(board)
        scores = {col: 0 for col in valid_moves}
        for col in valid_moves:
            for _ in range(self.simulations):
                scores[col] += self.simulate_game(board, col, player)
        return max(scores, key=scores.get)

monte_carlo_ai = MonteCarloAI(simulations=100)

# Game Initialization
board = create_board()
game_over = False
turn = np.random.randint(2)

# Main game loop
draw_board(board)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, SQUARESIZE // 2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER)
                    if winning_move(board, PLAYER):
                        label = myfont.render("Player 1 wins!", True, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn = AI
                    draw_board(board)

    if turn == AI and not game_over:
        col = monte_carlo_ai.best_move(board, AI)
        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI)
            if winning_move(board, AI):
                label = myfont.render("AI wins!", True, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            draw_board(board)
            turn = PLAYER

    clock.tick(30)

    if game_over:
        pygame.time.wait(3000)
