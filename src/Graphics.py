import pygame


def calculateSquare(pos, size):
    return (int(pos[0]/size), int(8 - pos[1]/size))

def loadAssets(size):
    whitePawn = pygame.image.load("src/assets/Chess_plt60.png")
    whitePawn = pygame.transform.scale(whitePawn, (size, size))
    blackPawn = pygame.image.load("src/assets/Chess_pdt60.png")
    blackPawn = pygame.transform.scale(blackPawn, (size, size))
    whiteRook = pygame.image.load("src/assets/Chess_rlt60.png")
    whiteRook = pygame.transform.scale(whiteRook, (size, size))
    blackRook = pygame.image.load("src/assets/Chess_rdt60.png")
    blackRook = pygame.transform.scale(blackRook, (size, size))
    whiteKnight = pygame.image.load("src/assets/Chess_nlt60.png")
    whiteKnight = pygame.transform.scale(whiteKnight, (size, size))
    blackKnight = pygame.image.load("src/assets/Chess_ndt60.png")
    blackKnight = pygame.transform.scale(blackKnight, (size, size))
    whiteBishop = pygame.image.load("src/assets/Chess_blt60.png")
    whiteBishop = pygame.transform.scale(whiteBishop, (size, size))
    blackBishop = pygame.image.load("src/assets/Chess_bdt60.png")
    blackBishop = pygame.transform.scale(blackBishop, (size, size))
    whiteQueen = pygame.image.load("src/assets/Chess_qlt60.png")
    whiteQueen = pygame.transform.scale(whiteQueen, (size, size))
    blackQueen = pygame.image.load("src/assets/Chess_qdt60.png")
    blackQueen = pygame.transform.scale(blackQueen, (size, size))
    whiteKing = pygame.image.load("src/assets/Chess_klt60.png")
    whiteKing = pygame.transform.scale(whiteKing, (size, size))
    blackKing = pygame.image.load("src/assets/Chess_kdt60.png")
    blackKing = pygame.transform.scale(blackKing, (size, size))
    whiteSquare = pygame.image.load("src/assets/whiteSq.png")
    whiteSquare = pygame.transform.scale(whiteSquare, (size, size))
    blackSquare = pygame.image.load("src/assets/blackSq.png")
    blackSquare = pygame.transform.scale(blackSquare, (size, size))

    return [None, whitePawn, whiteRook, whiteKnight, whiteBishop, whiteQueen, whiteKing, whiteSquare, blackSquare, None, None, blackPawn, blackRook, 
    blackKnight, blackBishop, blackQueen, blackKing]

def printBoard(screen, assets, board, size):
    screen.fill((0, 0, 0))
    for i in range(7, -1, -1):
        for j in range(8):
            x = j
            y = 7 - i
            if (x + y)%2 == 0:
                screen.blit(assets[7], (x*size, y*size))
            else:
                screen.blit(assets[8], (x*size, y*size))
            if board.heldPiece and j == board.heldPiece[0] and i == board.heldPiece[1]:
                continue
            if board.board[j][i]:
                screen.blit(assets[board.board[j][i]], (x*size, y*size))