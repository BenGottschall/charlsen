import chess
import chess.svg
from chess_board import ChessBoard
from bot import ChessBot
from human import HumanPlayer
from board_renderer import BoardRenderer
import pygame
import os
import config

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

IS_BOT = False  # Set to False for human vs bot, True for bot vs bot

class ChessGame:
    def __init__(self, fen = None):
        self.board = ChessBoard() if not fen else ChessBoard(fen)
        self.WINDOW_SIZE = config.BOARD_SIZE
        self.spritesheet = pygame.image.load(f"{ASSETS_DIR}/spritesheet.png")
        self.board_renderer = BoardRenderer(self.board.board, self.spritesheet, self.WINDOW_SIZE)

        
        # Initialize players based on IS_BOT flag
        if IS_BOT:
            self.white_player = ChessBot()
            self.black_player = ChessBot()
        else:
            self.white_player = HumanPlayer(chess.WHITE, self, self.board_renderer)
            self.black_player = ChessBot()
        
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound(f"{ASSETS_DIR}/move-self.mp3")
        self.capture_sound = pygame.mixer.Sound(f"{ASSETS_DIR}/capture.mp3")
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Chess Game")
        # self.board_surf = self.board_renderer.create_board_surface()


    def display_board(self, last_move=None, dragging=False,
                      mouse_pos=None, selected_square=None):
        """Display the current board state"""
        # Build highlight dictionary for the selected square
        highlight_squares = {}
        selected_piece = None

        if selected_square is not None:
            highlight_squares = {move.to_square: "#aaa23b80" for move in self.board.get_board_state().legal_moves if
                                 move.from_square == selected_square}
            selected_piece = self.board.get_board_state().piece_at(selected_square)
            piece_color = "w" if selected_piece.color else "b"
            selected_piece = f"{piece_color}{selected_piece.symbol().lower()}"

        if last_move is not None:
            highlight_squares[last_move.from_square] = "#fd705f80"
            highlight_squares[last_move.to_square] = "#fd705f80"

        self.board_renderer.draw_board(self.screen)
        self.board_renderer.draw_pieces(self.screen, selected_square, fill=highlight_squares)

        if dragging:
            self.board_renderer.draw_drag(self.screen, mouse_pos, selected_piece)

        pygame.display.flip()

    def play_move_sound(self, move):
        """plays move sound"""
        if self.board.board.is_capture(move):
            print("capture move")
            self.capture_sound.play()
        else:
            self.move_sound.play()

    def play_game(self):
        """Main game loop"""
        last_move = None
        self.black_player.start_game_log(f"{LOGS_DIR}/minimax.log")

        while not self.board.is_game_over():
            # Get current player for selected square highlighting
            current_player = self.white_player if self.board.get_board_state().turn else self.black_player
            selected_square = getattr(current_player, 'selected_square', None)
            dragging = getattr(current_player, 'dragging', False)
            print(f"Current player: {current_player}\ndragging: {dragging}")

            # Display current board with highlights
            self.display_board(last_move, dragging, selected_square)

            # Determine current player
            current_player = self.white_player if self.board.get_board_state().turn else self.black_player

            # Get player's move
            move = current_player.get_move(self.board)

            if move is None:
                print("Game ended by player")
                break

            self.play_move_sound(move)
            # Make the move
            if not self.board.make_move(move):
                print(f"Illegal move attempted: {move}")
                break


            print(f"Move played: {move}")
            last_move = move

            # Add delay only for bot moves
            if isinstance(current_player, ChessBot):
                pygame.time.wait(100)  # .1 second delay

        # Display final position
        self.display_board(last_move)
        result = self.board.get_result()
        print(f"Game Over! Result: {result}")

        # Keep window open until closed
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break

        pygame.quit()


if __name__ == "__main__":
    fen = "6k1/8/q3K3/8/4B3/8/8/2q5 w - - 0 1"
    game = ChessGame()
    game.play_game()
