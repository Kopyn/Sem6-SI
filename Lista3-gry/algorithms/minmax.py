from copy import deepcopy
from numpy import Infinity
from checkers.board import Board
from checkers.constants import BLACK, WHITE
from checkers.piece import Piece

skipped = False


def minmax(position : Board, depth, maximizing_player):
    skipped = False
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    if maximizing_player:
        max_eval = -Infinity
        best_move = None
        for child in get_all_moves(WHITE, position):
            minmax_val = minmax(child, depth - 1, False)
            evaluation = minmax_val[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = child
        if position.white_left + position.black_left != best_move.white_left + best_move.black_left:
            skipped = True
        return (max_eval, best_move, skipped)
    else:
        min_eval = Infinity
        best_move = None
        for child in get_all_moves(BLACK, position):
            minmax_val = minmax(child, depth - 1, True)
            evaluation = minmax_val[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = child
            if position.white_left + position.black_left != best_move.white_left + best_move.black_left:
                skipped = True
        return (min_eval, best_move, skipped)

def minmax1(position : Board, depth, maximizing_player):
    skipped = False
    if depth == 0 or position.winner() != None:
        return position.evaluate1(), position
    if maximizing_player:
        max_eval = -Infinity
        best_move = None
        for child in get_all_moves(WHITE, position):
            minmax_val = minmax(child, depth - 1, False)
            evaluation = minmax_val[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = child
        if position.white_left + position.black_left != best_move.white_left + best_move.black_left:
            skipped = True
        return (max_eval, best_move, skipped)
    else:
        min_eval = Infinity
        best_move = None
        for child in get_all_moves(BLACK, position):
            minmax_val = minmax(child, depth - 1, True)
            evaluation = minmax_val[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = child
            if position.white_left + position.black_left != best_move.white_left + best_move.black_left:
                skipped = True
        return (min_eval, best_move, skipped)

def get_all_moves(color, board : Board):
    possible_moves = board.get_game_valid_moves(color)
    returned_moves = []
    for moves in possible_moves:
        row, col = moves[0], moves[1]
        for move in possible_moves[moves]:
            copied_board: Board = deepcopy(board)
            returned_moves.append(simulate_move(copied_board.get_piece(row, col), move, copied_board, possible_moves[moves][move])[0])
    return returned_moves

def simulate_move(piece : Piece, move, board, skipped) -> Board:
    board.move(piece, move[0], move[1])
    if_king = piece.king
    if skipped:
        board.remove(skipped)
    return board, if_king
