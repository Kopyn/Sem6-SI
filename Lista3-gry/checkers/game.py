import random
import time
from matplotlib.animation import MovieWriter
import pygame

from checkers.board import Board
from checkers.piece import Piece
from checkers.constants import BLACK, BLUE, SQUARE_SIZE, WHITE

class Game:
    def __init__(self, window):
        self.init_game()
        self.window = window
        self.white_moves = 0
        self.black_moves = 0
        self.white_total = time.time()
        self.black_total = time.time()

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def init_game(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.game_valid_moves = self.get_valid_piece_moves(self.turn)
        self.moved = False
        self.king_moves_without_capture = 0

    def winner(self):
        return self.board.winner()

    def reset(self):
        self.init_game()

    def select(self, row, col) -> bool:
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
                self.moved = False
            else:
                self.moved = True
        piece = self.board.get_piece(row, col)
        
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            if (row, col) in self.game_valid_moves.keys():
                self.valid_moves = self.game_valid_moves[(row, col)]
                return True
            else:
                self.valid_moves = {}
            return False
        return False

    def move(self, row, col):
        piece : Piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
                if piece != 0:
                    if piece.king:
                        self.king_moves_without_capture = 0
            else:
                if piece != 0:
                    if piece.king:
                        self.king_moves_without_capture += 1
                    else:
                        self.king_moves_without_capture = 0
            self.change_turn()
            return True
        else:
            return False

    def ai_move(self, board):
        if self.turn == BLACK:
            self.black_moves += 1
        else:
            self.white_moves += 1
        self.board = board
        self.change_turn()

    def make_random_move(self):
        keys = self.get_valid_piece_moves(WHITE).keys()
        piece = random.choice(list(keys))
        moves = self.get_valid_piece_moves(WHITE)[(piece[0], piece[1])]
        move = random.choice(list(moves))
        self.select(piece[0], piece[1])
        self.select(move[0], move[1])

    def get_valid_piece_moves(self, color):
        return self.board.get_game_valid_moves(color)

    def change_turn(self):
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK
        self.game_valid_moves = self.get_valid_piece_moves(self.turn)
        self.valid_moves = {}

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
        