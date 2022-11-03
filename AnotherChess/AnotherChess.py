from math import trunc
from sqlite3 import IntegrityError
from Board import *
import pygame, sys

pygame.init()
size = WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = 60
black = 0, 0, 0

whitePawn = pygame.image.load("assets/Chess_plt60.png")        # probably do this in some other file at some point
blackPawn = pygame.image.load("assets/Chess_pdt60.png")
whiteRook = pygame.image.load("assets/Chess_rlt60.png")
blackRook = pygame.image.load("assets/Chess_rdt60.png")
whiteKnight = pygame.image.load("assets/Chess_nlt60.png")
blackKnight = pygame.image.load("assets/Chess_ndt60.png")
whiteBishop = pygame.image.load("assets/Chess_blt60.png")
blackBishop = pygame.image.load("assets/Chess_bdt60.png")
whiteQueen = pygame.image.load("assets/Chess_qlt60.png")
blackQueen = pygame.image.load("assets/Chess_qdt60.png")
whiteKing = pygame.image.load("assets/Chess_klt60.png")
blackKing = pygame.image.load("assets/Chess_kdt60.png")
whiteSquare = pygame.image.load("assets/whiteSq.png")
whiteSquare = pygame.transform.scale(whiteSquare, (60, 60))
blackSquare = pygame.image.load("assets/blackSq.png")
blackSquare = pygame.transform.scale(blackSquare, (60, 60))

assets = [None, whitePawn, whiteRook, whiteKnight, whiteBishop, whiteQueen, whiteKing, whiteSquare, blackSquare, None, None, blackPawn, blackRook, 
blackKnight, blackBishop, blackQueen, blackKing]

screen = pygame.display.set_mode(size)
board = Board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    board.printBoard(screen, assets, SQUARE_SIZE)
    pygame.display.flip()
