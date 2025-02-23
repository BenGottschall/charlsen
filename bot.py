import chess
from chess_board import ChessBoard

class ChessBot:
    def __init__(self):
        pass

    def score_move(self, board: chess.Board, move: chess.Move) -> int:
        piece_values = {
            1: 100, 2: 320, 3: 330,
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

    def evaluate_position(self, board: chess.Board) -> int:
        """
        Evaluates the current position of the board.
        Positive values favor white, negative values favor black.
        :param board: chess.Board object (not ChessBoard)
        :return: score representing the current position
        """

        if board.is_game_over():
            if board.is_checkmate():

                return -10000 if board.turn else 10000
            return 0 # Draw

        score = 0
        piece_values = {
            1 : 100, 2 : 300, 3 : 300,
            4 : 500, 5 : 900, 6 : 20000
        }

        for piece in piece_values:
            score += len(board.pieces(piece, True)) * piece_values[piece]
            score -= len(board.pieces(piece, False)) * piece_values[piece]

        return score

    def minimax(self, board: chess.Board, depth, alpha, beta, maximizing_player) -> (int, chess.Move):
        """
        Minimax implementation.
        Returns (best_score, best_move)
        """

        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        best_move = None

        # Gather moves and sort them
        moves = list(board.legal_moves)
        moves.sort(key=lambda m: self.score_move(board, m), reverse=True)

        if maximizing_player:
            best_eval = float('-inf')
            for move in moves:
                board.push(move)
                score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()

                if score > best_eval:
                    best_eval = score
                    best_move = move

                if best_eval > alpha:
                    alpha = best_eval

                if alpha >= beta:
                    break

            return best_eval, best_move
        else:
            best_eval = float('inf')
            for move in moves:
                board.push(move)
                score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()

                if score < best_eval:
                    best_eval = score
                    best_move = move

                if best_eval < beta:
                    beta = best_eval

                if beta <= alpha:
                    break

            return best_eval, best_move

    def negamax(self, board: chess.Board, depth, alpha, beta) -> (int, chess.Move):
        """
        Negamax implementation.
        Returns the best evaluation
        """

        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        best_move = None
        best_eval = float('-inf')

        # Gather moves and sort them
        moves = list(board.legal_moves)
        moves.sort(key=lambda m: self.score_move(board, m), reverse=True)

        for move in moves:
            board.push(move)
            score, _ = self.negamax(board, depth - 1, -beta, -alpha)
            score = -score
            board.pop()

            if score > best_eval:
                best_eval = score
                best_move = move

                if score > alpha:
                    alpha = score

            if score >= beta:
                return best_eval, best_move

        return best_eval, best_move




    def get_move(self, board: ChessBoard) -> chess.Move:
        """
        Main method to select the best move.
        """
        state = board.get_board_state()

        eval_n, move_n = self.negamax(state, depth=4, alpha=float("inf"), beta=-float("inf"))

        eval_m, move_m = self.minimax(state, depth=4, alpha=-float('inf'), beta=float('inf'), maximizing_player=board.get_board_state().turn)



        # Each time you pick a move for logging:
        self.log_move(move_m, eval_m, move_n, eval_n)

        print(f"Player: {state.turn}")
        print(f"Best move: {move_n}, Evaluation: {eval_n}")
        return move_m



    def start_game_log(self, filename="minimax_vs_negamax.log"):
        # "w" mode overwrites the file or creates it if it doesn't exist
        with open(filename, "w") as log_file:
            log_file.write("Starting a new game...\n\n")

    def log_move(self, minimax_move, eval_m, negamax_move, eval_n, filename="minimax_vs_negamax.log"):
        # "a" mode appends new lines without removing what's already there
        with open(filename, "a") as log_file:
            log_file.write(f"Minimax move: {minimax_move}, eval: {eval_m}\n")
            log_file.write(f"Negamax move: {negamax_move}, eval: {eval_n}\n\n")