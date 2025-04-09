import chess
from .chess_board import ChessBoard
from .evaluation import Evaluation
from .opening_book import OpeningBook
import time

class ChessBot:
    def __init__(self):
        self.log_file = "None"
        self.transposition_table = {}
        self.evaluation = Evaluation()
        self.opening_book = OpeningBook("../assets/Book.txt")

    def score_move(self, board: chess.Board, move: chess.Move) -> int:
        """
        TODO: Probably move this to some sort of ordering moves file/class
        :param board: chess.Board object holding game state
        :param move: chess.Move object holding move to be scored
        :return: score of the move
        """
        piece_values = {
            1: 100, 2: 300, 3: 300,
            4: 500, 5: 900, 6: 20000
        }
        score = 0;
        # Check if it’s a capture
        if board.is_capture(move):
            captured_piece_type = board.piece_type_at(move.to_square)
            if captured_piece_type:
                score += piece_values[captured_piece_type]

            moving_piece = board.piece_type_at(move.from_square)
            if moving_piece:
                score -= piece_values[moving_piece] // 10  # reduce the value by some fraction of the capturer

        # Check for promotion
        if move.promotion:
            # Queen promotion is typically best
            if move.promotion == chess.QUEEN:
                score += 800  # big boost
            else:
                score += 200  # smaller boost

        return score

    def get_transposition_key(self, board: chess.Board, depth: int, maximizing_player: bool):
        """
        Create a unique key for the transposition table
        Use board FEN for position, depth, and player to create a unique key
        TODO: Move this to a class, I don't think it does much at the moment
        """

        return (board.fen(), depth, maximizing_player)

    def minimax(self, board: chess.Board, depth, alpha, beta, maximizing_player, ply=0) -> (int, chess.Move):
        """
        Minimax implementation.
        Returns (best_score, best_move)
        """

        if depth == 0 or board.is_game_over():
            return self.evaluation.evaluate_position(board, ply, maximizing_player), None

        tt_key = self.get_transposition_key(board, depth, maximizing_player)

        if tt_key in self.transposition_table:
            return self.transposition_table[tt_key]

        best_move = None

        # Gather moves and sort them
        moves = list(board.legal_moves)
        moves.sort(key=lambda m: self.score_move(board, m), reverse=True)

        if maximizing_player:
            best_eval = float('-inf')
            for move in moves:
                board.push(move)
                score, _ = self.minimax(board, depth - 1, alpha, beta, False, ply+1)
                board.pop()

                if score > best_eval:
                    best_eval = score
                    best_move = move

                if best_eval > alpha:
                    alpha = best_eval

                if alpha >= beta:
                    break

            # Store result in transposition table
            self.transposition_table[tt_key] = (best_eval, best_move)
            return best_eval, best_move
        else:
            best_eval = float('inf')
            for move in moves:
                board.push(move)
                score, _ = self.minimax(board, depth - 1, alpha, beta, True, ply+1)
                board.pop()

                if score < best_eval:
                    best_eval = score
                    best_move = move

                if best_eval < beta:
                    beta = best_eval

                if beta <= alpha:
                    break
            # Store result in transposition table
            self.transposition_table[tt_key] = (best_eval, best_move)
            return best_eval, best_move

    def get_move(self, board: ChessBoard) -> chess.Move:
        """
        Main method to select the best move.
        """
        state = board.get_board_state()

        book_move = self.opening_book.get_move(state.fen())

        if book_move:
            return chess.Move.from_uci(book_move)

        print("no book move found")

        start_time = time.time()
        eval_m, move_m = self.minimax(state, depth=5, alpha=-float('inf'), beta=float('inf'), maximizing_player=board.get_board_state().turn)
        time_taken = time.time() - start_time


        # Each time you pick a move for logging:
        self.log_move(move_m, eval_m)

        print(f"Player: {state.turn}")
        print(f"Best move: {move_m}, Evaluation: {eval_m}, found in {time_taken:.4f} seconds.")
        return move_m



    def start_game_log(self, filename="minimax_vs_negamax.log"):
        self.log_file = filename
        # "w" mode overwrites the file or creates it if it doesn't exist
        with open(filename, "w") as log_file:
            log_file.write("Starting a new game...\n\n")

    def log_move(self, minimax_move, eval_m):
        # "a" mode appends new lines without removing what's already there

        with open(self.log_file, "a") as log_file:
            log_file.write(f"Minimax move: {minimax_move}, eval: {eval_m}\n\n")