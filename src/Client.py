import berserk
import threading
import logging
from Graphics import *

class Client:
    token, session, client = None, None, None
    gameId = None

    def __init__(self):
        with open('lichess.token') as f: self.token = f.read()
        self.session = berserk.TokenSession(self.token)
        self.client = berserk.Client(self.session)
        logging.basicConfig(filename='src/logs/client.log', encoding='utf-8', level=logging.DEBUG)

    def searchGame(self, clock, increment):
        print("seek time: ", self.client.board.seek(clock, increment))

    def clientMove(self, move):
        self.client.board.make_move(self.gameId, move)

    def clientResign(self):
        self.client.board.resign_game(self.gameId)

    def eventStream(self, board, menuTable, mixer, gs, cs):
        logging.info('event stream thread started')
        while True:
            for event in self.client.board.stream_incoming_events():
                print(event)
                eventType = event['type']
                if eventType == "gameStart":
                    self.gameId = event['game']['gameId']
                    if not event['game']['isMyTurn']: board.flip()
                    else: board.onlineTurn = True
                    gst = threading.Thread(target=self.gameStateStream, args=(board, menuTable, mixer, gs, cs), daemon=True)
                    gst.start()
                    logging.info('starting gs thread')
                else:
                    self.gameId = None
                    logging.info('game ended, resettting gameID. Awaiting gst')
                    gst.join()
                    logging.info('gst joined, awaiting event')
            
    def gameStateStream(self, board, menuTable, mixer, gs, cs):
        while self.gameId:
            for event in self.client.board.stream_game_state(self.gameId):
                print(event)
                eventType = event['type']
                if eventType == "gameState":
                    if not board.onlineTurn:
                        #print("{1}'s time left: {0}".format(event['game']['secondsLeft'], event['game']['opponent']['username']))
                        move = event['moves'].split(' ')[-1]
                        c = board.storage.uciToCoords(move)
                        m = board.tryMove(c[0], c[1], c[2])
                        if m: 
                            updateTable(menuTable)
                            mixer.playMove(m[0], m[1])
                            if m[2]: guiButtons[1].enable()
                            board.onlineTurn = True
                        cs = gs.REFRESH
                    else:
                        #print("your time left: {0}".format(event['game']['secondsLeft']))
                        board.onlineTurn = False
                elif eventType == "chatLine":
                    print(event)

