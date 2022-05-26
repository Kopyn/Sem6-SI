from copy import deepcopy
import pygame
from .piece import Piece
from .constants import BLACK, WHITE, RED, ROWS, SQUARE_SIZE, COLS, GREY

class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()

    def draw_board(self, window):
        window.fill(GREY)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_board(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def winner(self):
        if self.white_left <= 0 or not self.get_game_valid_moves(BLACK):
            return WHITE
        elif self.black_left <=0 or not self.get_game_valid_moves(WHITE):
            return BLACK
        return None

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece: Piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 and piece.color == WHITE:
            piece.transform_to_king()
            if not piece.king:
                self.white_kings += 1
        if row == 0 and piece.color == BLACK:
            piece.transform_to_king()
            if not piece.king:
                self.black_kings += 1 

    def evaluate(self):
        # return self.white_left - self.black_left + (self.white_kings * 0.5 - self.black_kings * 0.5)
        return self.white_left - self.black_left

    def evaluate1(self):
        sumWhite = 0
        sumBlack = 0
        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == WHITE:
                        sumWhite += self.positionValue(piece)
                    else:
                        sumBlack += self.positionValue(piece)
        return self.white_left + sumWhite - self.black_left - sumBlack

    def positionValue(self, piece: Piece) -> int:
        if piece.row > 1 and piece.row < 6 and piece.col > 1 and piece.col < 6:
            return 3
        elif (piece.row == 1 or piece.row == 6) and (piece.col == 1 or piece.col == 6):
            return 2
        else:
            return 1

    def evaluate2(self):
        # return self.white_left - self.black_left + (self.white_kings * 0.5 - self.black_kings * 0.5)
        return self.white_left - self.black_left

    def remove(self, pieces : Piece):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                    if piece.king:
                        self.black_kings -= 1
                else:
                    self.white_left -= 1
                    if piece.king:
                        self.white_kings -= 1

    def get_valid_moves(self, piece):
        moves = {}
        moves.update(self.test_valid_moves(piece.row, piece.col, piece.color, False, -1, piece.row, piece.col))
        return moves

    def get_game_valid_moves(self, color):
        pieces = self.get_all_pieces(color)
        all_moves = {}
        returned_moves = {}
        for piece in pieces:
            all_moves[(piece.row, piece.col)] = self.get_valid_moves(piece)
        all_moves = {k : v for k, v in sorted(all_moves.items(), key = lambda item: -1 * self.get_move_length(item[1]))}
        length = 0
        for move in all_moves:
            result = self.get_move_length(all_moves[move])
            l = result[0]
            if l > length:
                length = l
        for move in all_moves:
            result = self.get_move_length(all_moves[move])
            if result[0] == length:
                returned_moves[move] = self.filter_moves(all_moves[move], result[0])
        return returned_moves

    def filter_moves(self, move, length):
        returned_moves = {}
        for m in move:
            if len(move[m]) == length:
                returned_moves[m]=move[m]
        return returned_moves

    def get_move_length(self, moves):
        m = (-1, -1)
        length = -1
        for move in moves:
            if len(moves[move]) > length:
                length = len(moves[move])
                m = move
        return length, m
    
    # variant is variable to describe where we jumped before not to "go back" to the same place after a jump
    # 1 - jumped upwards left
    # 2 - jumped upwards right
    # 3 - jumped downwards left
    # 4 - jumped downwards right
    def test_valid_moves(self, row, col, color, skipped : bool, variant : int, start_row, start_col, skipped_pieces = []):
        moves = {}
        if self.get_piece(row, col).king:
            moves.update(self.queen_move_upwards_left(row, col, color))
            moves.update(self.queen_move_upwards_right(row, col, color))
            moves.update(self.queen_move_downwards_left(row, col, color))
            moves.update(self.queen_move_downwards_right(row, col, color))
        else:
            if variant != 4:
                moves.update(self.jump_upwards_left(row, col, color, start_row, start_col, []))
            if variant != 3:
                moves.update(self.jump_upwards_right(row, col, color, start_row, start_col, []))
            if variant != 2:
                moves.update(self.jump_downwards_left(row, col, color, start_row, start_col, []))
            if variant != 1:
                moves.update(self.jump_downwards_right(row, col, color, start_row, start_col, []))
            if not skipped:
                moves.update(self.move_left(row, col, color))
                moves.update(self.move_right(row, col, color))
        return moves

    def jump(self, row, col, color, skipped : bool, variant : int, start_row, start_col, skipped_pieces = []):
        copied = deepcopy(skipped_pieces)
        moves = {}
        if len(skipped_pieces) >= 5:
            return moves
        if variant != 4:
            moves.update(self.jump_upwards_left(row, col, color, start_row, start_col, copied))
        if variant != 3:
            moves.update(self.jump_upwards_right(row, col, color, start_row, start_col, copied))
        if variant != 2:
            moves.update(self.jump_downwards_left(row, col, color, start_row, start_col, copied))
        if variant != 1:
            moves.update(self.jump_downwards_right(row, col, color, start_row, start_col, copied))

        return moves

    def queen_move_upwards_left(self, row, col, color):
        moves = {}
        r = row
        c = col
        while r > 0 and c > 0:
            r -= 1
            c -= 1
            if self.board[r][c] == 0:
                moves[(r, c)] = []
            else:
                if self.get_piece(r, c).color != color:
                    moves.update(self.jump_upwards_left(r+1, c+1, color, row, col, []))
                    # moves.update(self.jump(r + 1, c + 1, color, False, 3, row, col, []))
                    break
                else:
                    break
        return moves

    def queen_move_upwards_right(self, row, col, color):
        moves = {}
        r = row
        c = col
        while r > 0 and c < COLS - 1:
            r -= 1
            c += 1
            if self.board[r][c] == 0:
                moves[(r, c)] = []
            else:
                if self.get_piece(r, c).color != color:
                    moves.update(self.jump_upwards_right(r+1, c-1, color, row, col, []))
                    # moves.update(self.jump(r + 1, c - 1, color, False, 4, row, col, []))
                    break
                else:
                    break
        return moves

    def queen_move_downwards_left(self, row, col, color):
        moves = {}
        r = row
        c = col
        while r < ROWS - 1 and c > 0:
            r += 1
            c -= 1
            if self.board[r][c] == 0:
                moves[(r, c)] = []
            else:
                if self.get_piece(r, c).color != color:
                    moves.update(self.jump_downwards_left(r-1, c+1, color, row, col, []))
                    # moves.update(self.jump(r - 1, c + 1, color, False, 1, row, col, []))
                    break
                else:
                    break
        return moves

    def queen_move_downwards_right(self, row, col, color):
        moves = {}
        r = row
        c = col
        while r < ROWS - 1 and c < COLS - 1:
            r += 1
            c += 1
            if self.board[r][c] == 0:
                moves[(r, c)] = []
            else:
                if self.get_piece(r, c).color != color:
                    moves.update(self.jump_downwards_right(r-1, c-1, color, row, col, []))
                    # moves.update(self.jump(r - 1, c - 1, color, False, -1, row, col, []))
                    break
                else:
                    break
        return moves

    def move_left(self, row, col, color):
        moves = {}
        if color == BLACK:
            if row > 0 and col > 0 and self.board[row - 1][col - 1] == 0:
                moves[(row - 1, col - 1)] = []
        else:
            if row < ROWS - 1 and col > 0 and self.board[row + 1][col - 1] == 0:
                moves[(row + 1, col - 1)] = []
        return moves

    def move_right(self, row, col, color):
        moves = {}
        if color == BLACK:
            if row > 0 and col < COLS - 1 and self.board[row - 1][col + 1] == 0:
                moves[(row - 1, col + 1)] = []
        else:
            if row < ROWS - 1 and col < COLS - 1 and self.board[row + 1][col + 1] == 0:
                moves[(row + 1, col + 1)] = []
        return moves


    def jump_upwards_left(self, row, col, color, start_row, start_col, skipped_pieces, last_skipped = 0):
        moves = {}
        copied = deepcopy(skipped_pieces)
        if row > 0 and col > 0 and self.board[row - 1][col - 1] != 0:
            if self.board[row - 1][col - 1].color != color:
                if row - 1 > 0 and col - 1 > 0 and self.board[row - 2][col - 2] == 0:
                    copied.append(self.board[row - 1][col - 1])
                    # moves[(row, col)] = skipped_pieces
                    moves.update(self.jump(row - 2, col - 2, color, True, 1, start_row, start_col, copied))
            else:
                if row != start_row or col != start_col:
                    moves[(row, col)] = skipped_pieces
        else:
            if row != start_row or col != start_col:
                moves[(row, col)] = skipped_pieces
        # moves[(row - 2, col - 2)] = skipped_pieces 
        return moves

    def jump_upwards_right(self, row, col, color, start_row, start_col, skipped_pieces, last_skipped = 0):
        moves = {}
        copied = deepcopy(skipped_pieces)
        if row > 0 and col < COLS - 1 and self.board[row - 1][col + 1] != 0:
            if self.board[row - 1][col + 1].color != color:
                if row - 1 > 0 and col + 1 < COLS - 1 and self.board[row - 2][col + 2] == 0:
                    copied.append(self.board[row - 1][col + 1])
                    # moves[(row, col)] = skipped_pieces
                    moves.update(self.jump(row - 2, col + 2, color, True, 2, start_row, start_col, copied))
            else:
                if row != start_row or col != start_col:
                    moves[(row, col)] = skipped_pieces
        else:
            if row != start_row or col != start_col:
                moves[(row, col)] = skipped_pieces
        # moves[(row - 2, col + 2)] = skipped_pieces 
        return moves

    def jump_downwards_left(self, row, col, color, start_row, start_col, skipped_pieces, last_skipped = 0):
        moves = {}
        copied = deepcopy(skipped_pieces)
        if row < ROWS - 1 and col > 0 and self.board[row + 1][col - 1] != 0:
            if self.board[row + 1][col - 1].color != color:
                if row + 1 < ROWS - 1 and col - 1 > 0 and self.board[row + 2][col - 2] == 0:
                    copied.append(self.board[row + 1][col - 1])
                    # moves[(row, col)] = skipped_pieces
                    moves.update(self.jump(row + 2, col - 2, color, True, 3, start_row, start_col, copied))
            else:
                if row != start_row or col != start_col:
                    moves[(row, col)] = skipped_pieces
        else:
            if row != start_row or col != start_col:
                moves[(row, col)] = skipped_pieces
        # moves[(row + 2, col - 2)] = skipped_pieces 
        return moves

    def jump_downwards_right(self, row, col, color, start_row, start_col, skipped_pieces, last_skipped = 0):
        moves = {}
        copied = deepcopy(skipped_pieces)
        if row < ROWS - 1 and col < COLS - 1 and self.board[row + 1][col + 1] != 0:
            if self.board[row + 1][col + 1].color != color:
                if row + 1 < ROWS - 1 and col + 1 < COLS - 1 and self.board[row + 2][col + 2] == 0:
                    copied.append(self.board[row + 1][col + 1])
                    # moves[(row, col)] = skipped_pieces
                    moves.update(self.jump(row + 2, col + 2, color, True, 4, start_row, start_col, copied))
            else:
                if row != start_row or col != start_col:
                    moves[(row, col)] = skipped_pieces
        else:
            if row != start_row or col != start_col:
                moves[(row, col)] = skipped_pieces
        # moves[(row + 2, col + 2)] = skipped_pieces 
        return moves

    def __repr__(self):
        representation = ""
        for row in self.board:
            representation += str(row)
            representation += "\n"
        return representation