import pygame


def calculateSquare(pos, board, size):
    if (not board.flipped):
        return (int(pos[0]/size), int(8 - pos[1]/size))
    return (7 - int(pos[0]/size), 7 - int(8 - pos[1]/size))

def inBounds(pos, size):
    for i in range(2):
        if pos[i] > size * 7.56:
            pos[i] = size * 7.56
        elif pos[i] < 0:
            pos[i] = 0

def loadAssets(size):
    o = [None for i in range(17)]
    team = ['l', 'd']
    pieces = [None, 'p', 'r', 'n', 'b', 'q', 'k']

    for i in range(1, 7):
        for j in range(2):
            o[i + 10*j] = pygame.transform.scale(pygame.image.load("src/assets/Chess_" + pieces[i] + team[j] + "t60.png"), (size, size))

    whiteSquare = pygame.image.load("src/assets/whiteSq.png")
    whiteSquare = pygame.transform.scale(whiteSquare, (size, size))
    blackSquare = pygame.image.load("src/assets/blackSq.png")
    blackSquare = pygame.transform.scale(blackSquare, (size, size))

    o[7] = whiteSquare
    o[8] = blackSquare

    return o

def printBoard(screen, assets, board, size):
    screen.fill((255, 255, 255), (0, 0, size*8, size*8))
    for i in range(7, -1, -1):
        for j in range(8):
            x = j
            y = 7 - i
            if board.flipped:
                x = 7-x
                y = 7-y
            if (x + y)%2 == 0:
                screen.blit(assets[7], (x*size, y*size))
            else:
                screen.blit(assets[8], (x*size, y*size))
            if board.heldPiece and j == board.heldPiece[0] and i == board.heldPiece[1]:
                continue
            if board.board[j][i]:
                screen.blit(assets[board.board[j][i]], (x*size, y*size))

