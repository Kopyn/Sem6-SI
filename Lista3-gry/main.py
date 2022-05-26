import pygame
from algorithms.minmax import minmax, minmax1
from algorithms.alphabeta import alphabeta, alphabeta1
from checkers.constants import BLACK, SQUARE_SIZE, WIDTH, HEIGHT, WHITE
from checkers.board import Board
from checkers.game import Game
from numpy import Infinity
import algorithms
import time

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Warcaby")

FPS = 100

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def ai_ai(depth1 : int, depth2 : int):
    clock = pygame.time.Clock()
    board = Board()
    game_run = True
    game = Game(WINDOW)
    time.sleep(2.0)
    white_total = 0
    black_total = 0
    first_move = True
    move_counter = 0

    game.update()

    while game_run:
        # clock.tick(FPS)
        currentTime = time.time()
        if first_move:
            game.make_random_move()
            first_move = False
            pass
        else:
            package = minmax1(game.board, depth1, True)
            game.ai_move(package[1])
            if package[2] == False:
                move_counter += 1
            else:
                move_counter = 0
        white_total += (time.time() - currentTime)
        game.update()
        # time.sleep(0.3)
        
        if game.winner() != None:
            print(game.winner())
            game_run = False
            break
        
        currentTime = time.time()
        package = minmax1(game.board, depth2, False)
        game.ai_move(package[1])
        if package[2] == False:
            move_counter += 1
        else:
            move_counter = 0
        black_total += (time.time() - currentTime)
        game.update()
        # time.sleep(0.3)

        if game.winner() != None:
            print(game.winner())
            game_run = False
            break
        if move_counter >= 30:
            game_run = False
            print("Draw")
            break
    time.sleep(5)
    pygame.quit()
    print("White total time: ")
    print(white_total)
    print("Black total time: ")
    print(black_total)
    print("Moves: ")
    if game.winner() == BLACK:
        print(game.black_moves)
    else:
        print(game.white_moves)

    print("black moves: ", game.black_moves)
    print("white moves: ", game.white_moves)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def ai_ai_ab(depth1 : int, depth2 : int):
    clock = pygame.time.Clock()
    board = Board()
    game_run = True
    game = Game(WINDOW)
    time.sleep(2.0)
    white_total = 0
    black_total = 0
    first_move = True
    move_counter = 0

    game.update()

    while game_run:
        # clock.tick(FPS)
        currentTime = time.time()
        if first_move:
            game.make_random_move()
            first_move = False
            pass
        else:
            package = minmax1(game.board, depth1, True)
            game.ai_move(package[1])
            if package[2] == False:
                move_counter += 1
            else:
                move_counter = 0
        white_total += (time.time() - currentTime)
        game.update()
        # time.sleep(0.3)
        
        if game.winner() != None:
            print(game.winner())
            game_run = False
            break
        
        currentTime = time.time()
        package = alphabeta1(game.board, depth2, -Infinity, Infinity, False)
        game.ai_move(package[1])
        if package[2] == False:
            move_counter += 1
        else:
            move_counter = 0
        black_total += (time.time() - currentTime)
        game.update()
        # time.sleep(0.3)

        if game.winner() != None:
            print(game.winner())
            game_run = False
            break
        if move_counter >= 30:
            game_run = False
            print("Draw")
            break
    time.sleep(5)
    pygame.quit()
    print("White total time: ")
    print(white_total)
    print("Black total time: ")
    print(black_total)
    print("Moves: ")
    if game.winner() == BLACK:
        print(game.black_moves)
    else:
        print(game.white_moves)

def player_ai(depth : int, turn):
    clock = pygame.time.Clock()
    board = Board()
    game_run = True
    game = Game(WINDOW)

    game.update()

    player_turn = not turn

    while game_run:
        # clock.tick(FPS)

        if player_turn:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    print((row, col))
                    # piece = board.get_piece(row, col)
                    # board.move(piece, 4, 3)
                    game.select(row, col)
            game.update()
            if game.winner() != None:
                print(game.winner())
                game_run = False
            if game.moved:
                player_turn = False
        else:
            game.ai_move(minmax(game.board, depth, turn)[1])
            game.moved = False
            game.update()

            if game.winner() != None:
                print(game.winner())
                game_run = False
                break
            player_turn = True

        # board.draw_board(WINDOW)
        # board.draw(WINDOW)
        # pygame.display.update()
    
    pygame.quit()

def ai_ai_alphabeta(depth1 : int, depth2 : int):
    clock = pygame.time.Clock()
    board = Board()
    game_run = True
    game = Game(WINDOW)
    time.sleep(2.0)
    white_total = 0
    black_total = 0
    first_move = True
    move_counter = 0

    game.update()

    while game_run:
        # clock.tick(FPS)
        currentTime = time.time()
        # package = 0
        if first_move:
            game.make_random_move()
            first_move = False
            pass
        else:
            package = alphabeta(game.board, depth1, -Infinity, Infinity, True)
            game.ai_move(package[1])
            if package[2] == False:
                move_counter += 1
            else:
                move_counter = 0
        white_total += (time.time() - currentTime)
        game.update()
        # time.sleep(0.3)
        
        if game.winner() != None:
            print(game.winner())
            game_run = False
            break

        currentTime = time.time()
        package = alphabeta(game.board, depth2, -Infinity, Infinity, False)
        game.ai_move(package[1])
        if package[2] == False:
            move_counter += 1
        else:
            move_counter = 0
        black_total += (time.time() - currentTime)
        game.update()
        # time.sleep(0.3)

        if game.winner() != None:
            print(game.winner())
            game_run = False
            break
        
        if move_counter >= 30:
            game_run = False
            print("Draw")
            break
        print(move_counter)
    time.sleep(5)
    pygame.quit()
    print("White total time: ")
    print(white_total)
    print("Black total time: ")
    print(black_total)
    print("Moves: ")
    if game.winner() == BLACK:
        print(game.black_moves)
    else:
        print(game.white_moves)

def player_ai_alphabeta(depth : int, turn):
    clock = pygame.time.Clock()
    board = Board()
    game_run = True
    game = Game(WINDOW)

    game.update()

    player_turn = not turn

    while game_run:
        # clock.tick(FPS)

        if player_turn:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    print((row, col))
                    # piece = board.get_piece(row, col)
                    # board.move(piece, 4, 3)
                    game.select(row, col)
            game.update()
            if game.winner() != None:
                print(game.winner())
                game_run = False
            if game.moved:
                player_turn = False
        else:
            game.ai_move(alphabeta(game.board, depth, -Infinity, Infinity, turn)[1])
            game.moved = False
            game.update()

            if game.winner() != None:
                print(game.winner())
                game_run = False
                break
            player_turn = True

        # board.draw_board(WINDOW)
        # board.draw(WINDOW)
        # pygame.display.update()
    
    pygame.quit()

def player_player():
    clock = pygame.time.Clock()
    board = Board()
    game_run = True
    game = Game(WINDOW)

    while game_run:
        # clock.tick(FPS)

        for event in pygame.event.get():

            if game.winner() != None:
                print(game.winner())
                game_run = False

            if event.type == pygame.QUIT:
                game_run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                print((row, col))
                # piece = board.get_piece(row, col)
                # board.move(piece, 4, 3)
                game.select(row, col)
        
        game.update()

        # board.draw_board(WINDOW)
        # board.draw(WINDOW)
        # pygame.display.update()
    time.sleep(5)
    pygame.quit()

if __name__ == "__main__":

    dic = {(5,0):{(4,1):[]}, (5,2):{(4,1):[]}}
    for key in dic:
        print(key)

    # player_player()
    # player_ai(3, True)
    # ai_ai(3, 3)
    ai_ai_ab(3, 3)
    # player_ai_alphabeta(3, True)
    # ai_ai_alphabeta(5, 5)