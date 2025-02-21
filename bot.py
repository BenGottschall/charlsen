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

    def minimax(self, board: chess.Board, depth, alpha, beta, maximizing_player) -> (int, chess.Move):
        """
        Minimax implementation.
        Returns (best_score, best_move)
        """

        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_move(self, board: ChessBoard) -> chess.Move:
        """
        Main method to select the best move.
        """
        evaluation, best_move = self.minimax(board.board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=board.get_board_state().turn)
        print(f"Player: {board.get_board_state().turn}")
        print(f"Best move: {best_move}, Evaluation: {evaluation}")
        return best_move