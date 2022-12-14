from math import trunc
from sqlite3 import IntegrityError
from Board import *
from Graphics import *
from Sound import *
from enum import Enum
import pygame, sys
import pygame_gui

pygame.init()
size = WIDTH, HEIGHT = 625, 600
SQUARE_SIZE = 60
black = 0, 0, 0

piece = 0
assets = loadAssets(SQUARE_SIZE)
gameState = Enum('gameState', ['REFRESH', 'STANDBY', 'PICKUP', 'HOLDPIECE', 'PUTDOWN', 'PROMOTE'])

currentState = gameState.REFRESH

screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'src/theme.json')
clock = pygame.time.Clock()
board = Board()
mixer = SoundMixer()

flipButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 100), (100, 50)), text='flip', manager=manager)
newGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 175), (100, 50)), text='new game', manager=manager)
newGameButton.disable()

promoteButtons = 0
promotePiece = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if currentState == gameState.PROMOTE:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(promoteButtons):
                    if event.ui_element == button:
                        board.tryMove(board.heldPiece, promotePiece, i)
                        piece = 0
                        for p in promoteButtons: p.kill()
                        promoteButtons = 0
                        board.placePiece()
                        board.turn = not board.turn
                        currentState = gameState.REFRESH
                        break
            manager.process_events(event)
            continue
        if event.type == pygame.MOUSEBUTTONDOWN: currentState = gameState.PICKUP
        if event.type == pygame.MOUSEBUTTONUP: currentState = gameState.PUTDOWN
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == flipButton:
                board.flip()
                currentState = gameState.REFRESH
            if event.ui_element == newGameButton:
                board = Board()
                currentState == gameState.REFRESH
                newGameButton.disable()

        manager.process_events(event)

    if (currentState == gameState.PICKUP):
        pos = pygame.mouse.get_pos()
        coords = calculateSquare(pos, board, SQUARE_SIZE)
        if (coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7):
            currentState = gameState.STANDBY
            continue
        if (board.board[coords[0]][coords[1]]): 
            piece = board.pickupPiece(coords)
        currentState = gameState.HOLDPIECE

    elif (currentState == gameState.HOLDPIECE):
        if (piece):
            pos = pygame.mouse.get_pos()
            printBoard(screen, assets, board, SQUARE_SIZE)
            adjustedPos = list(pos)
            inBounds(adjustedPos, SQUARE_SIZE)
            screen.blit(assets[piece], (adjustedPos[0] - SQUARE_SIZE/2, adjustedPos[1] - SQUARE_SIZE/2))

    elif (currentState == gameState.PUTDOWN):
        if (piece):
            pos = pygame.mouse.get_pos()
            coords = calculateSquare(pos, board, SQUARE_SIZE)
            if (coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7):
                pass
            elif (piece % 10 == 1 and (coords[1] == 0 or coords[1] == 7)):
                printBoard(screen, assets, board, SQUARE_SIZE)
                currentState = gameState.PROMOTE
                promoteButtons = generateButtons(manager, board, coords, SQUARE_SIZE)
                promotePiece = coords
            else:
                m = board.tryMove(board.heldPiece, coords, None)
                if m: mixer.playMove(m[0], m[1])
        if not promoteButtons:
            piece = 0
            board.placePiece()
            currentState = gameState.REFRESH

    elif (currentState == gameState.PROMOTE):
        time_delta = clock.tick(60)/1000.0
        manager.update(time_delta)
        manager.draw_ui(screen)

    elif (currentState == gameState.REFRESH):
        printBoard(screen, assets, board, SQUARE_SIZE)
        currentState = gameState.STANDBY

    elif (currentState == gameState.STANDBY):
        time_delta = clock.tick(60)/1000.0
        manager.update(time_delta)
        manager.draw_ui(screen)

    pygame.display.update()