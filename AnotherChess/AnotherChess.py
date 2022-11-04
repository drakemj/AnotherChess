from math import trunc
from sqlite3 import IntegrityError
from Board import *
from enum import Enum
import pygame, sys

pygame.init()
size = WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = 60
black = 0, 0, 0
piece = 0
pieceLocation = 0
gameState = Enum('gameState', ['REFRESH', 'STANDBY', 'PICKUP', 'HOLDPIECE', 'PUTDOWN'])
currentState = gameState.REFRESH

whitePawn = pygame.image.load("AnotherChess/assets/Chess_plt60.png")        # probably do this in some other file at some point
blackPawn = pygame.image.load("AnotherChess/assets/Chess_pdt60.png")
whiteRook = pygame.image.load("AnotherChess/assets/Chess_rlt60.png")
blackRook = pygame.image.load("AnotherChess/assets/Chess_rdt60.png")
whiteKnight = pygame.image.load("AnotherChess/assets/Chess_nlt60.png")
blackKnight = pygame.image.load("AnotherChess/assets/Chess_ndt60.png")
whiteBishop = pygame.image.load("AnotherChess/assets/Chess_blt60.png")
blackBishop = pygame.image.load("AnotherChess/assets/Chess_bdt60.png")
whiteQueen = pygame.image.load("AnotherChess/assets/Chess_qlt60.png")
blackQueen = pygame.image.load("AnotherChess/assets/Chess_qdt60.png")
whiteKing = pygame.image.load("AnotherChess/assets/Chess_klt60.png")
blackKing = pygame.image.load("AnotherChess/assets/Chess_kdt60.png")
whiteSquare = pygame.image.load("AnotherChess/assets/whiteSq.png")
whiteSquare = pygame.transform.scale(whiteSquare, (60, 60))
blackSquare = pygame.image.load("AnotherChess/assets/blackSq.png")
blackSquare = pygame.transform.scale(blackSquare, (60, 60))

assets = [None, whitePawn, whiteRook, whiteKnight, whiteBishop, whiteQueen, whiteKing, whiteSquare, blackSquare, None, None, blackPawn, blackRook, 
blackKnight, blackBishop, blackQueen, blackKing]

screen = pygame.display.set_mode(size)
board = Board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: currentState = gameState.PICKUP
        if event.type == pygame.MOUSEBUTTONUP: currentState = gameState.PUTDOWN

    if (currentState == gameState.PICKUP):
        pos = pygame.mouse.get_pos()
        coords = board.calculateSquare(pos, SQUARE_SIZE)
        if (board.board[coords[0]][coords[1]]): 
            piece = board.pickupPiece(coords)
            pieceLocation = coords
        currentState = gameState.HOLDPIECE

    elif (currentState == gameState.HOLDPIECE):
        if (piece):
            pos = pygame.mouse.get_pos()
            board.printBoard(screen, assets, SQUARE_SIZE)
            screen.blit(assets[piece], (pos[0] - SQUARE_SIZE/2, pos[1] - SQUARE_SIZE/2))
            pygame.display.flip()

    elif (currentState == gameState.PUTDOWN):
        if (piece):
            pos = pygame.mouse.get_pos()
            coords = board.calculateSquare(pos, SQUARE_SIZE)
            if board.availableMoves(pieceLocation[0], pieceLocation[1], piece)[coords[0]][coords[1]]: #kind of yucky. Ideally should
                board.board[coords[0]][coords[1]] = piece                 #make it so the board doesn't update until here in the first place
                board.turn = not board.turn
            else:
                board.board[pieceLocation[0]][pieceLocation[1]] = piece
        piece = 0
        pieceLocation = 0
        currentState = gameState.REFRESH

    elif (currentState == gameState.REFRESH):
        board.printBoard(screen, assets, SQUARE_SIZE)
        pygame.display.flip()
        currentState = gameState.STANDBY
