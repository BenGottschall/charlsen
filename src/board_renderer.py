import pygame
import chess

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
