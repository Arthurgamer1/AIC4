import numpy as np
import math

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0  # Minimax AI
AI = 1      # Monte Carlo AI
EMPTY = -1
WINDOW_LENGTH = 4

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

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

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

def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def get_ai_move(board, depth=5):
    col, _ = minimax(board, depth, -math.inf, math.inf, True)
    return col

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
def simulate_games(num_games):
    monte_carlo_wins = 0
    minimax_wins = 0
    draws = 0

    for game in range(num_games):
        print(f"Simulating game {game + 1} of {num_games}...")
        board = create_board()
        game_over = False
        turn = np.random.randint(2)  # Randomly choose who starts

        while not game_over:
            if turn == PLAYER:  # Minimax AI
                col = get_ai_move(board, depth=5)
            else:  # Monte Carlo AI
                col = monte_carlo_ai.best_move(board, AI)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn)

                if winning_move(board, turn):
                    game_over = True
                    if turn == PLAYER:
                        minimax_wins += 1
                    else:
                        monte_carlo_wins += 1

                elif len(get_valid_locations(board)) == 0:  # Draw
                    game_over = True
                    draws += 1

                turn = (turn + 1) % 2  # Switch turn

    print(f"\nSimulation Complete!\n")
    print(f"Monte Carlo AI Wins: {monte_carlo_wins}")
    print(f"Minimax AI Wins: {minimax_wins}")
    print(f"Draws: {draws}")

# Run the simulation
simulate_games(100)
