import random
import numpy as np

class Connect4:
    ROWS = 6
    COLS = 7
    EMPTY = 0

    def __init__(self):
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)

    def drop_piece(self, col, player):
        """Drop a piece into the specified column."""
        for row in reversed(range(self.ROWS)):
            if self.board[row, col] == self.EMPTY:
                self.board[row, col] = player
                return True
        return False

    def is_valid_move(self, col):
        """Check if a move is valid."""
        return self.board[0, col] == self.EMPTY

    def get_valid_moves(self):
        """Return a list of valid column indices."""
        return [col for col in range(self.COLS) if self.is_valid_move(col)]

    def check_winner(self, player):
        """Check if a player has won."""
        # Check horizontal, vertical, and diagonal lines
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if np.all(self.board[row, col:col+4] == player):
                    return True
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if np.all(self.board[row:row+4, col] == player):
                    return True
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if all(self.board[row + i, col + i] == player for i in range(4)):
                    return True
                if all(self.board[row + 3 - i, col + i] == player for i in range(4)):
                    return True
        return False

    def is_draw(self):
        """Check if the game is a draw."""
        return all(self.board[0, col] != self.EMPTY for col in range(self.COLS))

    def print_board(self):
        """Print the board to the console."""
        print(np.flip(self.board, 0))

class MonteCarloAI:
    def __init__(self, simulations=100):
        self.simulations = simulations

    def simulate_game(self, board, col, player):
        """Simulate a random game from the current state."""
        simulated_board = np.copy(board)
        connect4 = Connect4()
        connect4.board = simulated_board

        if not connect4.drop_piece(col, player):
            return 0  # Invalid move

        opponent = 3 - player
        while True:
            if connect4.check_winner(player):
                return 1  # Win
            if connect4.check_winner(opponent):
                return -1  # Loss
            if connect4.is_draw():
                return 0  # Draw

            valid_moves = connect4.get_valid_moves()
            if not valid_moves:
                break
            move = random.choice(valid_moves)
            connect4.drop_piece(move, opponent)
            player, opponent = opponent, player

        return 0

    def best_move(self, board, player):
        """Find the best move using Monte Carlo simulations."""
        valid_moves = [col for col in range(Connect4.COLS) if board[0, col] == Connect4.EMPTY]
        scores = {col: 0 for col in valid_moves}

        for col in valid_moves:
            for _ in range(self.simulations):
                scores[col] += self.simulate_game(board, col, player)

        return max(scores, key=scores.get)

# Game Loop
def play_game():
    game = Connect4()
    ai = MonteCarloAI(simulations=100)
    human_player = 1
    ai_player = 2

    print("Welcome to Connect 4!")
    game.print_board()

    while True:
        # Human Move
        print("Your turn!")
        valid_moves = game.get_valid_moves()
        print(f"Valid moves: {valid_moves}")
        move = int(input("Enter your move (0-6): "))
        while move not in valid_moves:
            move = int(input("Invalid move. Enter a valid move (0-6): "))
        game.drop_piece(move, human_player)
        game.print_board()

        if game.check_winner(human_player):
            print("You win!")
            break
        if game.is_draw():
            print("It's a draw!")
            break

        # AI Move
        print("AI's turn...")
        ai_move = ai.best_move(game.board, ai_player)
        game.drop_piece(ai_move, ai_player)
        game.print_board()

        if game.check_winner(ai_player):
            print("AI wins!")
            break
        if game.is_draw():
            print("It's a draw!")
            break

play_game()
