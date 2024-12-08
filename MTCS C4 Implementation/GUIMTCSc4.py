import pygame
import numpy as np
import random

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BOARD_ROWS = 6
BOARD_COLS = 7
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 5
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Connect4:
    EMPTY = 0

    def __init__(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)

    def drop_piece(self, col, player):
        for row in reversed(range(BOARD_ROWS)):
            if self.board[row, col] == self.EMPTY:
                self.board[row, col] = player
                return True
        return False

    def is_valid_move(self, col):
        return self.board[0, col] == self.EMPTY

    def get_valid_moves(self):
        return [col for col in range(BOARD_COLS) if self.is_valid_move(col)]

    def check_winner(self, player):
        # Horizontal, vertical, and diagonal checks
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS - 3):
                if np.all(self.board[row, col : col + 4] == player):
                    return True
        for row in range(BOARD_ROWS - 3):
            for col in range(BOARD_COLS):
                if np.all(self.board[row : row + 4, col] == player):
                    return True
        for row in range(BOARD_ROWS - 3):
            for col in range(BOARD_COLS - 3):
                if all(self.board[row + i, col + i] == player for i in range(4)):
                    return True
                if all(self.board[row + 3 - i, col + i] == player for i in range(4)):
                    return True
        return False

    def is_draw(self):
        return all(self.board[0, col] != self.EMPTY for col in range(BOARD_COLS))


class MonteCarloAI:
    def __init__(self, simulations=100):
        self.simulations = simulations

    def simulate_game(self, board, col, player):
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
        valid_moves = [
            col for col in range(BOARD_COLS) if board[0, col] == Connect4.EMPTY
        ]
        scores = {col: 0 for col in valid_moves}

        for col in valid_moves:
            for _ in range(self.simulations):
                scores[col] += self.simulate_game(board, col, player)

        return max(scores, key=scores.get)


def draw_board(screen, game):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            pygame.draw.rect(
                screen,
                BLUE,
                (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            color = BLACK
            if game.board[row, col] == 1:
                color = RED
            elif game.board[row, col] == 2:
                color = YELLOW
            pygame.draw.circle(
                screen,
                color,
                (
                    col * CELL_SIZE + CELL_SIZE // 2,
                    row * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2,
                ),
                RADIUS,
            )


def draw_menu(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Connect 4", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
    button = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 3, 60)
    pygame.draw.rect(screen, BLUE, button)
    text = font.render("Play", True, WHITE)
    screen.blit(
        text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 10)
    )
    return button


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Connect 4")
    clock = pygame.time.Clock()
    game = Connect4()
    ai = MonteCarloAI()
    human_player = 1
    ai_player = 2

    # Menu
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        play_button = draw_menu(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    menu_running = False

    # Game Loop
    game_running = True
    turn = 1  # Human starts
    while game_running:
        screen.fill(BLACK)
        draw_board(screen, game)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if turn == human_player and event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                col = x_pos // CELL_SIZE
                if game.is_valid_move(col):
                    game.drop_piece(col, human_player)
                    if game.check_winner(human_player):
                        print("You win!")
                        game_running = False
                    elif game.is_draw():
                        print("It's a draw!")
                        game_running = False
                    turn = ai_player

        if turn == ai_player and game_running:
            pygame.time.wait(500)
            col = ai.best_move(game.board, ai_player)
            game.drop_piece(col, ai_player)
            if game.check_winner(ai_player):
                print("AI wins!")
                game_running = False
            elif game.is_draw():
                print("It's a draw!")
                game_running = False
            turn = human_player

        clock.tick(60)


if __name__ == "__main__":
    main()
