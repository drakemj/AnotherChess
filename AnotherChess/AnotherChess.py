from Board import *

board = Board()
board.printBoard()

print()
board.turn = False
board.printBoard(board.availableMoves(6, 7))