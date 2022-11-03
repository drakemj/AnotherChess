from math import trunc
from sqlite3 import IntegrityError
from Board import *
import pygame, sys

pygame.init()
size = WIDTH, HEIGHT = 400, 400
black = 0, 0, 0

whitePawn = pygame.image.load("assets/Chess_plt60.png")        # probably do this in some other file at some point
blackPawn = pygame.image.load("assets/Chess_pdt60.png")
whiteRook = pygame.image.load("assets/Chess_rlt60.png")
blackRook = pygame.image.load("assets/Chess_rdt60.png")
whiteKnight = pygame.image.load("assets/Chess_klt60.png")
blackKnight = pygame.image.load("assets/Chess_kdt60.png")
whiteBishop = pygame.image.load("assets/Chess_blt60.png")
blackBishop = pygame.image.load("assets/Chess_bdt60.png")
whiteQueen = pygame.image.load("assets/Chess_qlt60.png")
blackQueen = pygame.image.load("assets/Chess_qdt60.png")
whiteKing = pygame.image.load("assets/Chess_klt60.png")
blackKing = pygame.image.load("assets/Chess_kdt60.png")
whiteSquare = pygame.image.load("assets/whiteSq.png")
blackSquare = pygame.image.load("assets/blackSq.png")

assets = [None, whitePawn, whiteRook, whiteKnight, whiteBishop, whiteQueen, whiteKing, whiteSquare, blackSquare, None, blackPawn, blackRook, 
blackKnight, blackBishop, blackQueen, blackQueen]

screen = pygame.display.set_mode(size)
board = Board()
board.printBoard()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    screen.blit(assets[1], (0, 0))
    pygame.display.flip()
