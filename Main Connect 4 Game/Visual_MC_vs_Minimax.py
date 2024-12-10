import pygame
import numpy as np
import math
import random

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0  # Minimax AI
AI = 1      # Monte Carlo AI
EMPTY = -1
WINDOW_LENGTH = 4
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
MARGIN = 5
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Initialize pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four: Minimax vs Monte Carlo")

# Game functions
def create_board():
    return np.full((ROW_COUNT, COLUMN_COUNT), EMPTY)

def draw_board(board):
    # Draw the names of the AI algorithms
    font = pygame.font.SysFont("monospace", 20)
    
    # Text showing which AI corresponds to which color
    text_minimax = font.render("Minimax AI (Red)", True, RED)
    text_montecarlo = font.render("Monte Carlo AI (Yellow)", True, YELLOW)
    
    # Display the text at the top of the screen
    screen.blit(text_minimax, (10, 10))  # Minimax at the top left
    screen.blit(text_montecarlo, (width - text_montecarlo.get_width() - 10, 10))  # Monte Carlo at the top right

    # Draw the empty board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int((ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    # Draw the pieces on the board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int((ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int((ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.display.update()

def display_winner(winner):
    font = pygame.font.SysFont("monospace", 40)
    
    if winner == PLAYER:
        message = "Minimax AI (Red) Wins!"
        color = RED  # Set color to Red for Minimax
    elif winner == AI:
        message = "Monte Carlo AI (Yellow) Wins!"
        color = YELLOW  # Set color to Yellow for Monte Carlo
    else:
        message = "It's a Draw!"
        color = WHITE  # Draw message in white
    
    # Render the text
    text = font.render(message, True, color)
    
    # Display the message at the top of the screen
    screen.blit(text, (width // 2 - text.get_width() // 2, 40))  # 10 pixels from the top
    
    pygame.display.update()

    # Wait for a few seconds before closing
    pygame.time.wait(3000)



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
            if board[r][c] == piece and all(board[r][c+i] == piece for i in range(1, 4)):
                return True

    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and all(board[r+i][c] == piece for i in range(1, 4)):
                return True

    # Positive diagonal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and all(board[r+i][c+i] == piece for i in range(1, 4)):
                return True

    # Negative diagonal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and all(board[r-i][c+i] == piece for i in range(1, 4)):
                return True

    return False

def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER):
                return (None, -10000000000000)
            else:  # No more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI))

    if maximizingPlayer:
        value = -math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
def evaluate_window(window, piece):
    score = 0
    opponent = PLAYER if piece == AI else AI

    # Count the number of piece and opponent piece in the window
    piece_count = window.count(piece)
    opponent_count = window.count(opponent)

    # If there's a 4-in-a-row, return a large positive score for the player or negative for the opponent
    if piece_count == 4:
        score += 100
    elif opponent_count == 4:
        score -= 100

    # If there's a 3-in-a-row with one empty space, it's a good position for the player
    elif piece_count == 3 and window.count(EMPTY) == 1:
        score += 5
    elif opponent_count == 3 and window.count(EMPTY) == 1:
        score -= 5

    # If there's a 2-in-a-row with two empty spaces, it's a good position for the player
    elif piece_count == 2 and window.count(EMPTY) == 2:
        score += 2
    elif opponent_count == 2 and window.count(EMPTY) == 2:
        score -= 2

    return score


def score_position(board, piece):
    score = 0

    # Center column preference
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal scoring
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vertical scoring
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positive diagonal scoring
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Negative diagonal scoring
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER) or winning_move(board, AI) or len(get_valid_locations(board)) == 0

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

# Simulate games
def simulate_game():
    board = create_board()
    game_over = False
    turn = random.randint(0, 1)  # Randomly choose who starts

    while not game_over:
        draw_board(board)
        pygame.display.update()

        if turn == PLAYER:  # Minimax AI
            col, _ = minimax(board, 5, -math.inf, math.inf, True)
        else:  # Monte Carlo AI
            col = monte_carlo_ai.best_move(board, AI)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, turn)

            if winning_move(board, turn):
                draw_board(board)
                pygame.display.update()
                display_winner(turn)  # Display the winner
                game_over = True
            elif len(get_valid_locations(board)) == 0:  # Draw
                draw_board(board)
                pygame.display.update()
                display_winner(None)  # Display draw
                game_over = True

            turn = (turn + 1) % 2  # Switch turn


# Main loop to start the game
simulate_game()
pygame.time.wait(5000)  # Wait for 10 seconds before closing the window
pygame.quit()
