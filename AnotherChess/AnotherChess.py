from math import trunc
from sqlite3 import IntegrityError
from Board import *
from Graphics import *
from enum import Enum
import pygame, sys

pygame.init()
size = WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = 60
black = 0, 0, 0

piece = 0
pieceLocation = 0
assets = loadAssets(SQUARE_SIZE)
gameState = Enum('gameState', ['REFRESH', 'STANDBY', 'PICKUP', 'HOLDPIECE', 'PUTDOWN'])

currentState = gameState.REFRESH

screen = pygame.display.set_mode(size)
board = Board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: currentState = gameState.PICKUP
        if event.type == pygame.MOUSEBUTTONUP: currentState = gameState.PUTDOWN

    if (currentState == gameState.PICKUP):
        pos = pygame.mouse.get_pos()
        coords = calculateSquare(pos, SQUARE_SIZE)
        if (board.board[coords[0]][coords[1]]): 
            piece = board.pickupPiece(coords)
            pieceLocation = coords
        currentState = gameState.HOLDPIECE

    elif (currentState == gameState.HOLDPIECE):
        if (piece):
            pos = pygame.mouse.get_pos()
            printBoard(screen, assets, board, SQUARE_SIZE)
            screen.blit(assets[piece], (pos[0] - SQUARE_SIZE/2, pos[1] - SQUARE_SIZE/2))
            pygame.display.flip()

    elif (currentState == gameState.PUTDOWN):
        if (piece):
            pos = pygame.mouse.get_pos()
            coords = calculateSquare(pos, SQUARE_SIZE)
            if board.availableMoves(pieceLocation[0], pieceLocation[1], piece)[coords[0]][coords[1]]: #kind of yucky. Ideally should
                board.board[coords[0]][coords[1]] = piece                 #make it so the board doesn't update until here in the first place
                board.turn = not board.turn
            else:
                board.board[pieceLocation[0]][pieceLocation[1]] = piece
        piece = 0
        pieceLocation = 0
        currentState = gameState.REFRESH

    elif (currentState == gameState.REFRESH):
        printBoard(screen, assets, board, SQUARE_SIZE)
        pygame.display.flip()
        currentState = gameState.STANDBY
