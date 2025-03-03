class PieceTable:
    """Stores and manages piece tables for evaluation"""

    PAWNS_MID = 0
    PAWNS_END = 1
    KNIGHTS = 2
    BISHOPS = 3
    ROOKS = 4
    QUEENS = 5
    KING_EARLY = 6
    KING_END = 7

    def __init__(self):
        self.tables = {
            False: {
                self.PAWNS_MID: self._pawns_mid(),
                self.PAWNS_END: self._pawns_end(),
                self.KNIGHTS: self._knights(),
                self.BISHOPS: self._bishops(),
                self.ROOKS: self._rooks(),
                self.QUEENS: self._queens(),
                self.KING_EARLY: self._king_start(),
                self.KING_END: self._king_end(),
            }
        }
        self.tables[True] = self._invert_tables(self.tables[False])
        # False = white, True = black

    def read(self, color: bool, table, square):
        return self.tables[color][table][square]

    @staticmethod
    def _invert_tables(white_tables):
        return {piece: list(reversed(table)) for piece, table in white_tables.items()}

    @staticmethod
    def _pawns_mid():
        return [
            0,   0,   0,   0,   0,   0,   0,  0,
            50, 50,  50,  50,  50,  50,  50, 50,
            10, 10,  20,  30,  30,  20,  10, 10,
            5,   5,  10,  25,  25,  10,  5,   5,
            0,   0,   0,  20,  20,   0,  0,   0,
            5,  -5, -10,   0,   0, -10, -5,   5,
            5,  10,  10, -20, -20,  10, 10,   5,
            0,   0,   0,   0,   0,   0,  0,   0
        ]

    @staticmethod
    def _pawns_end():
        return [
             0,   0,   0,   0,   0,   0,   0,   0,
			80,  80,  80,  80,  80,  80,  80,  80,
			50,  50,  50,  50,  50,  50,  50,  50,
			30,  30,  30,  30,  30,  30,  30,  30,
			20,  20,  20,  20,  20,  20,  20,  20,
			10,  10,  10,  10,  10,  10,  10,  10,
			10,  10,  10,  10,  10,  10,  10,  10,
			 0,   0,   0,   0,   0,   0,   0,   0
        ]

    @staticmethod
    def _knights():
        return [
            -50,-40,-30,-30,-30,-30,-40,-50,
			-40,-20,  0,  0,  0,  0,-20,-40,
			-30,  0, 10, 15, 15, 10,  0,-30,
			-30,  5, 15, 20, 20, 15,  5,-30,
			-30,  0, 15, 20, 20, 15,  0,-30,
			-30,  5, 10, 15, 15, 10,  5,-30,
			-40,-20,  0,  5,  5,  0,-20,-40,
			-50,-40,-30,-30,-30,-30,-40,-50,
        ]

    @staticmethod
    def _bishops():
        return [
            -20,-10,-10,-10,-10,-10,-10,-20,
			-10,  0,  0,  0,  0,  0,  0,-10,
			-10,  0,  5, 10, 10,  5,  0,-10,
			-10,  5,  5, 10, 10,  5,  5,-10,
			-10,  0, 10, 10, 10, 10,  0,-10,
			-10, 10, 10, 10, 10, 10, 10,-10,
			-10,  5,  0,  0,  0,  0,  5,-10,
			-20,-10,-10,-10,-10,-10,-10,-20,
        ]

    @staticmethod
    def _rooks():
        return [
             0,  0,  0,  0,  0,  0,  0,  0,
			 5, 10, 10, 10, 10, 10, 10,  5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			 0,  0,  0,  5,  5,  0,  0,  0
        ]

    @staticmethod
    def _queens():
        return [
            -20,-10,-10, -5, -5,-10,-10,-20,
			-10,  0,  0,  0,  0,  0,  0,-10,
			-10,  0,  5,  5,  5,  5,  0,-10,
			-5,   0,  5,  5,  5,  5,  0, -5,
			 0,   0,  5,  5,  5,  5,  0, -5,
			-10,  5,  5,  5,  5,  5,  0,-10,
			-10,  0,  5,  0,  0,  0,  0,-10,
			-20,-10,-10, -5, -5,-10,-10,-20
        ]

    @staticmethod
    def _king_start():
        return [
            -80, -70, -70, -70, -70, -70, -70, -80,
			-60, -60, -60, -60, -60, -60, -60, -60,
			-40, -50, -50, -60, -60, -50, -50, -40,
			-30, -40, -40, -50, -50, -40, -40, -30,
			-20, -30, -30, -40, -40, -30, -30, -20,
			-10, -20, -20, -20, -20, -20, -20, -10,
			 20,  20,  -5,  -5,  -5,  -5,  20,  20,
			 20,  30,  10,   0,   0,  10,  30,  20
        ]

    @staticmethod
    def _king_end():
        return [
            -20, -10, -10, -10, -10, -10, -10, -20,
			 -5,   0,   5,   5,   5,   5,   0,  -5,
			-10, -5,   20,  30,  30,  20,  -5, -10,
			-15, -10,  35,  45,  45,  35, -10, -15,
			-20, -15,  30,  40,  40,  30, -15, -20,
			-25, -20,  20,  25,  25,  20, -20, -25,
			-30, -25,   0,   0,   0,   0, -25, -30,
			-50, -30, -30, -30, -30, -30, -30, -50
        ]