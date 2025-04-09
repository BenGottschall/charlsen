import chess
from .piece_table import PieceTable

class Evaluation:
    def __init__(self):
        self.piece_table = PieceTable()
        self.piece_values = {
            1: 100,
            2: 300,
            3: 300,
            4: 500,
            5: 900,
            6: 20000
        }

    def evaluate_position(self, board: chess.Board, depth_searched: int, color: bool) -> int:

        if board.is_game_over():
            if board.is_checkmate():
                return (-10000+depth_searched) if board.turn else (10000-depth_searched)
            return 0 # draw

        score = 0
        score += self.evaluate_material(board)
        score += self.evaluate_piece_tables(board, color)

        return score

    def evaluate_material(self, board: chess.Board) -> int:
        """simply counts the value of the material on the board"""
        score = 0
        for piece in self.piece_values:
            score += len(board.pieces(piece, True)) * self.piece_values[piece]
            score -= len(board.pieces(piece, False)) * self.piece_values[piece]
        return score

    def evaluate_piece_tables(self, board: chess.Board, color: bool) -> int:
        """
        evaluate all the piece tables
        TODO: Implement game phase, endgame pawns and king, for now only doing early game
        """
        score = 0

        score += self.evaluate_piece_table(board, self.piece_table.ROOKS, chess.ROOK, color)
        score += self.evaluate_piece_table(board, self.piece_table.KNIGHTS, chess.KNIGHT, color)
        score += self.evaluate_piece_table(board, self.piece_table.BISHOPS, chess.BISHOP, color)
        score += self.evaluate_piece_table(board, self.piece_table.QUEENS, chess.QUEEN, color)

        pawn_mid = self.evaluate_piece_table(board, self.piece_table.PAWNS_MID, chess.PAWN, color)
        pawn_late = self.evaluate_piece_table(board, self.piece_table.PAWNS_END, chess.PAWN, color)

        score += pawn_mid # change here later

        king_early = self.evaluate_piece_table(board, self.piece_table.KING_EARLY, chess.KING, color)
        king_late = self.evaluate_piece_table(board, self.piece_table.KING_END, chess.KING, color)

        score += king_early # also change here

        return score

    def evaluate_piece_table(self, board, table, piece_type: chess.PieceType, color: bool) -> int:
        score = 0

        for square in board.pieces(piece_type, color):
            score += self.piece_table.read(color, table, square)

        return score
