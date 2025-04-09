import pygame
import chess
import math

class BoardRenderer:
    def __init__(self, board, spritesheet, board_size=1200):
        self.board = board
        self.spritesheet = spritesheet
        self.square_size = board_size // 8
        self.board_size = board_size
        self.pieces = self.load_pieces()
        self.colors = {"square dark" : "#7e945e", "square light": "#eaecd3"}
        self.dragging = False

    def load_pieces(self):
        """Extracts and stores chess piece images from spritesheet."""
        piece_order = ["k", "q", "b", "n", "r", "p"]
        colors = { "w" : "white", "b" : "black"}
        piece_size = self.spritesheet.get_width() // 6
        pieces = {}

        for row, color in enumerate(["w", "b"]):
            for col, piece in enumerate(piece_order):
                rect = pygame.Rect(col * piece_size, row * piece_size, piece_size, piece_size)
                piece_image = self.spritesheet.subsurface(rect).copy()
                piece_image = pygame.transform.scale(piece_image, (self.square_size, self.square_size))
                pieces[f"{color}{piece}"] = piece_image
        print(pieces)
        return pieces

    def draw_board(self, screen):
        """Draws the chess board on the screen."""
        # square 0,0 is bottom left
        board_surf = pygame.Surface((self.square_size * 8, self.square_size * 8))
        for row in range(8):
            for col in range(8):
                color = self.colors["square dark"] if (row + col) % 2 else self.colors["square light"]
                pygame.draw.rect(board_surf, color,
                                 pygame.Rect(col * self.square_size, row * self.square_size, self.square_size,
                                             self.square_size))

        screen.blit(board_surf, (0,0))

    def draw_pieces(self, screen, selected_square=None, fill=None):
        """Places pieces on the board based on current board state"""
        if fill is not None:
            for square, color in fill.items():
                self.highlight_square(screen, color, 7-(square//8), (square%8))


        for square, piece in self.board.piece_map().items():
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            piece_key = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
            piece_image = self.pieces[piece_key]
            if square == selected_square:
                self.highlight_square(screen, "#38d3f450", row, col)
            screen.blit(piece_image, (col * self.square_size, row * self.square_size))


    def draw_drag(self, screen, mouse_pos, piece: str):
        """Draws the chess drag on the screen."""
        piece_image = self.pieces[piece]
        screen.blit(piece_image, (mouse_pos[0] - self.square_size // 2, mouse_pos[1] - self.square_size // 2))

    def highlight_square(self, screen, color, row, col):
        overlay = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        overlay.fill(color)
        screen.blit(overlay, (col * self.square_size, row * self.square_size))

    def draw_arrow(self, screen, arrow_surface, color, move):
        if isinstance(move, str):
            move = chess.Move.from_uci(move)

        from_sq = move.from_square
        to_sq = move.to_square

        from_x, from_y = self.square_to_pixel(from_sq)
        to_x, to_y = self.square_to_pixel(to_sq)

        dx = to_x - from_x
        dy = to_y - from_y
        length = math.hypot(dx, dy)
        if length == 0:
            return

        unit_dx = dx / length
        unit_dy = dy / length

        # Distance to pull back from the tip for the line
        arrow_size = 40
        arrow_offset = arrow_size * 0.6

        # Start and end of the line (arrow tip is dead center of destination square)
        start = (from_x + unit_dx * 10, from_y + unit_dy * 10)  # small offset from square center
        end = (to_x - unit_dx * arrow_offset, to_y - unit_dy * arrow_offset)

        # arrow_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        pygame.draw.line(arrow_surface, color, start, end, width=20)

        # Arrowhead centered in destination square
        arrow_tip = (to_x, to_y)

        angle = math.atan2(dy, dx)
        left = (
            arrow_tip[0] - arrow_size * math.cos(angle - math.pi / 5),
            arrow_tip[1] - arrow_size * math.sin(angle - math.pi / 5)
        )
        right = (
            arrow_tip[0] - arrow_size * math.cos(angle + math.pi / 5),
            arrow_tip[1] - arrow_size * math.sin(angle + math.pi / 5)
        )
        pygame.draw.polygon(arrow_surface, color, [arrow_tip, left, right])
        screen.blit(arrow_surface, (0, 0))

    def square_to_pixel(self, square):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        # Flip rank if board is displayed from White's perspective
        rank = 7 - rank
        return (file * self.square_size + self.square_size // 2,
                rank * self.square_size + self.square_size // 2)



# For testing (not working right now):
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    FEN = "8/8/2k5/8/4R3/3KR3/8/8 w - - 0 1"
    board = chess.Board()
    spritesheet = pygame.image.load("spritesheet.png")
    board_renderer = BoardRenderer(board, spritesheet, 800)


    running = True
    while running:
        board_renderer.draw_board(screen)
        board_renderer.draw_pieces(screen, dragging=True, mouse_pos=pygame.mouse.get_pos())
        board_renderer.draw_drag(screen, mouse_pos=pygame.mouse.get_pos())
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
