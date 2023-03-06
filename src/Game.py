from math import trunc
from sqlite3 import IntegrityError
from Board import *
from Graphics import *
from Sound import *
from Client import *
from enum import Enum
import pygame, sys
import pygame_gui
import threading

size = WIDTH, HEIGHT = 700, 625
SQUARE_SIZE = 60
black = 0, 0, 0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("AnotherChess Client")
        self.screen.fill((255, 255, 255))

        self.gameState = Enum('gameState', ['REFRESH', 'STANDBY', 'PICKUP', 'HOLDPIECE', 'PUTDOWN', 'PROMOTE'])

        self.currentState = self.gameState.REFRESH

        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'src/theme.json')
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.mixer = SoundMixer()
        self.network = Client()
        self.board.client = self.network

        self.graphics = Graphics(self)
        self.menuTable = self.graphics.menu
        self.assets = self.graphics.loadAssets(SQUARE_SIZE)

        self.threadQueue = []        # mutable data type for keeping track of data between threads in different files

        self.piece = 0
        self.promoteButtons = 0
        self.promoteSquare = 0

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: sys.exit()
                if self.currentState == self.gameState.PROMOTE:
                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        for i, button in enumerate(self.promoteButtons):
                            if event.ui_element == button:
                                self.board.finalizeMove(self.board.heldPiece, self.promoteSquare, i, self)
                                self.piece = 0
                                for p in self.promoteButtons: p.kill()
                                self.promoteButtons = 0
                                self.board.placePiece()
                                self.currentState = self.gameState.REFRESH
                                break
                    self.manager.process_events(event)
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    pos = pygame.mouse.get_pos()
                    coords = self.graphics.calculateSquare(pos, self.board, SQUARE_SIZE)
                    if (not self.board.inBounds(coords[0], coords[1]) or not self.board.isCurrentMove or (self.board.isOnline and not self.board.onlineTurn)):
                        self.currentState = self.gameState.STANDBY
                    else: self.currentState = self.gameState.PICKUP
                if event.type == pygame.MOUSEBUTTONUP: self.currentState = self.gameState.PUTDOWN
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.guiButtons[0]:       # flip
                        self.board.flip()
                    elif event.ui_element == self.guiButtons[1]:     # new game
                        for i in range(1, 4):
                            self.guiButtons[i].disable()
                        self.menuTable.clear()
                        self.menuTable.force_surface_update()
                        self.board.reset()
                    elif event.ui_element == self.guiButtons[2]:     # forward
                        if self.board.browseForward(): self.guiButtons[2].disable()   # think of more elegant solution
                        self.guiButtons[3].enable()
                        self.menuTable.select_widget(None)
                        self.menuTable.select_widget(str(self.board.ply))
                    elif event.ui_element == self.guiButtons[3]:     # back
                        if self.board.browseBack(): self.guiButtons[3].disable()
                        self.guiButtons[2].enable()
                        if (self.board.ply):
                            self.menuTable.select_widget(None) 
                            self.menuTable.select_widget(str(self.board.ply))
                    elif event.ui_element == self.guiButtons[4]:
                        self.guiButtons[4].disable()
                        searchGameThread = threading.Thread(target = self.network.searchGame, args=(10, 0), daemon=True)
                        searchGameThread.start()
                        self.board.isOnline = True
                        eventStreamThread = threading.Thread(target = self.network.eventStream, args=(self,), daemon=True)
                        eventStreamThread.start()
                    elif event.ui_element == self.guiButtons[5]:
                        if self.board.isOnline: 
                            self.network.clientResign()
                            self.guiButtons[1].enable()
                    self.currentState == self.gameState.REFRESH
                self.manager.process_events(event)

            if len(self.threadQueue):            # maybe support multiple items in queue in future, as needed
                if self.threadQueue[0] == 1:
                    self.currentState = self.gameState.REFRESH
                    self.threadQueue.clear()


            if (self.currentState == self.gameState.PICKUP):
                if (self.board.board[coords[0]][coords[1]]): 
                    self.piece = self.board.pickupPiece(coords)
                self.currentState = self.gameState.HOLDPIECE

            elif (self.currentState == self.gameState.HOLDPIECE):
                if (self.piece):
                    pos = pygame.mouse.get_pos()
                    self.graphics.printBoard(self.screen, self.assets, self.board, SQUARE_SIZE)
                    adjustedPos = list(pos)
                    self.graphics.makeInBounds(adjustedPos, SQUARE_SIZE)
                    self.screen.blit(self.assets[self.piece], (adjustedPos[0] - SQUARE_SIZE/2, adjustedPos[1] - SQUARE_SIZE/2))

            elif (self.currentState == self.gameState.PUTDOWN):
                if (self.piece):
                    pos = pygame.mouse.get_pos()
                    coords = self.graphics.calculateSquare(pos, self.board, SQUARE_SIZE)
                    if self.board.inBounds(coords[0], coords[1]):
                        if self.board.isPromotion(self.piece, coords):
                            if self.board.availableMoves(self.board.heldPiece[0], self.board.heldPiece[1])[coords[0]][coords[1]] and not self.board.moveInCheck(self.board.heldPiece, coords):
                                self.graphics.printBoard(self.screen, self.assets, self.board, SQUARE_SIZE)
                                self.currentState = self.gameState.PROMOTE
                                self.promoteButtons = self.graphics.generateButtons(self.manager, self.board, coords, SQUARE_SIZE)
                                self.promoteSquare = coords
                        else:
                            self.board.finalizeMove(self.board.heldPiece, coords, None, self)
                if not self.promoteButtons:
                    self.piece = 0
                    self.board.placePiece()
                    self.currentState = self.gameState.REFRESH

            elif (self.currentState == self.gameState.PROMOTE):
                time_delta = self.clock.tick(60)/1000.0
                self.manager.update(time_delta)
                self.manager.draw_ui(self.screen)

            elif (self.currentState == self.gameState.REFRESH):
                self.graphics.printBoard(self.screen, self.assets, self.board, SQUARE_SIZE)
                self.currentState = self.gameState.STANDBY

            elif (self.currentState == self.gameState.STANDBY):
                time_delta = self.clock.tick(60)/1000.0
                self.manager.update(time_delta)
                self.manager.draw_ui(self.screen)

            self.menuTable.update(events)
            self.menuTable.draw(self.screen)
            pygame.display.update()