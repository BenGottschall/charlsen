import chess
from chess_board import ChessBoard

class ChessBot:
    def __init__(self):
        pass

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
            1 : 100, 2 : 320, 3 : 330,
            4 : 500, 5 : 900, 6 : 20000
        }

        for piece in piece_values:
            score += len(board.pieces(piece, True)) * piece_values[piece]
            score -= len(board.pieces(piece, False)) * piece_values[piece]

        return score

    def negamax(self, board: chess.Board, depth, alpha, beta) -> int:
        """
        Negamax implementation.
        Returns the best evaluation
        """

        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board)

        legal_moves = board.legal_moves

        for move in legal_moves:
            board.push(move)
            evaluation = -self.negamax(board, depth - 1, -beta, -alpha)
            board.pop()

            if evaluation >= beta:
                return beta

            alpha = max(alpha, evaluation)

        return alpha


    def get_move(self, board: ChessBoard) -> chess.Move:
        """
        Main method to select the best move.
        """
        state = board.get_board_state()
        print(state.legal_moves)
        best_score = -float("inf")
        best_move = None

        for move in state.legal_moves:
            state.push(move)
            score = self.negamax(state, depth=4, alpha=-float("inf"), beta=float("inf"))
            score = -score  # Because of negamax symmetry
            state.pop()

            if score > best_score:
                best_score = score
                best_move = move

        print(f"Player: {state.turn}")
        print(f"Best move: {best_move}, Evaluation: {best_score}")
        return best_move