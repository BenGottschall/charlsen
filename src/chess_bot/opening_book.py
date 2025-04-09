import random
import pygame

class OpeningBook:
    def __init__(self, path):
        self.book = {}
        self.load_book(path)

    def load_book(self, path):
        current_fen = None
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('pos'):
                    current_fen = line[4:]
                    self.book[current_fen] = {}
                    # print(f"added fen: {current_fen}")
                elif current_fen:
                    move, freq = line.split()
                    self.book[current_fen][move] = int(freq)
                    # print(f"added move: {move}")

    def has_move(self, fen):
        return fen in self.book

    def get_move(self, fen):
        fen = ' '.join(fen.split(' ')[:4])

        if fen not in self.book:
            print(f"no fen: {fen}")
            return None

        moves = self.book[fen]
        total = sum(moves.values())
        rand_val = random.randint(1, total)
        cumulative = 0
        for move, freq in moves.items():
            cumulative += freq
            if rand_val <= cumulative:
                return move

        return None

    # def draw_book_moves(self, fen):
    #     if fen not in self.book:
    #         return None
    #
    #     moves = self.book[fen]
    #     for move, freq in moves.items():
    #         arrow_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)