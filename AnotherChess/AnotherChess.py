from math import trunc
from sqlite3 import IntegrityError
from Board import *
import pygame, sys

pygame.init()
size = width, height = 400, 400
black = 0, 0, 0

screen = pygame.display.set_mode(size)
board = Board()
board.printBoard()

def testInput(col, row):
    while (True):
        x = input()
        list = x.split(" ")
        if len(list) <= 1:
            print("not enough args")
            continue
        elif len(list) > 2:
            print("too many args")
            continue
        
        try:
            col = int(list[0])
            row = int(list[1])
        except:
            print("invalid input, only numbers 0-7")
            continue

        if col < 0 or col > 7 or row < 0 or row > 7:
            print("out of range")
            continue
        return [col, row]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    col = row = 0       #no turn checking even exists here
    print("select piece (col row): ")
    col, row = testInput(col, row)
    while board.board[col][row] == 0:
        print("invalid piece")
        col, row = testInput(col, row)  #again, probably change this. seems messy

    n_col = n_row = 0
    print("select move (col row): ")
    n_col, n_row = testInput(n_col, n_row)
    while board.availableMoves(col, row)[n_col][n_row] == 0: #creating new array every time. slow. also you can get softlocked if the piece has no moves
        print("invalid move")
        n_col, n_row = testInput(n_col, n_row)

    piece = board.board[col][row]      #will have a function eventually
    board.board[col][row] = 0
    board.board[n_col][n_row] = piece

    board.turn = not board.turn
    board.printBoard()

    screen.fill(black)
    pygame.display.flip()


