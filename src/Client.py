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
        self.client.challenges.create("daruxo", False, color=berserk.enums.Color.BLACK)
        # print("seek time: ", self.client.board.seek(clock, increment))

    def clientMove(self, move):
        self.client.board.make_move(self.gameId, move)

    def clientResign(self):
        self.client.board.resign_game(self.gameId)

    def eventStream(self, game):
        logging.info('event stream thread started')
        while True:
            for event in self.client.board.stream_incoming_events():
                print(event)
                eventType = event['type']
                if eventType == "gameStart":
                    self.gameId = event['game']['gameId']
                    if not event['game']['isMyTurn']: game.board.flip()
                    else: game.board.onlineTurn = True
                    gst = threading.Thread(target=self.gameStateStream, args=(game,), daemon=True)
                    gst.start()
                    game.threadQueue.append(1)        # update board in main thread
                    logging.info('starting gs thread')
                else:
                    if self.gameId:
                        self.gameId = None
                        logging.info('game ended, resetting gameID. Awaiting gst')
                        gst.join()
                        logging.info('gst joined, awaiting event')
            
    def gameStateStream(self, game):
        while self.gameId:
            for event in self.client.board.stream_game_state(self.gameId):
                eventType = event['type']
                if eventType == "gameState":
                    if not game.board.onlineTurn:
                        #print("{1}'s time left: {0}".format(event['game']['secondsLeft'], event['game']['opponent']['username']))
                        move = event['moves'].split(' ')[-1]
                        while not game.board.isCurrentMove: game.board.browseForward()
                        c = game.board.storage.uciToCoords(move)
                        game.board.finalizeMove(c[0], c[1], c[2], game)
                        game.board.onlineTurn = True
                        game.threadQueue.append(1)    # update board in main thread
                    else:
                        #print("your time left: {0}".format(event['game']['secondsLeft']))
                        game.board.onlineTurn = False
                elif eventType == "chatLine":
                    print(event)

