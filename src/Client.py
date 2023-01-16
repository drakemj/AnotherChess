import berserk
from Graphics import *

class Client:
    token, session, client = None, None, None
    gameId = None

    def __init__(self):
        with open('lichess.token') as f: self.token = f.read()
        self.session = berserk.TokenSession(self.token)
        self.client = berserk.Client(self.session)

    def searchGame(self, clock, increment):
        print("seek time: ", self.client.board.seek(clock, increment))

    def clientMove(self, move):
        self.client.board.make_move(self.gameId, move)

    def clientResign(self):
        self.client.board.resign_game(self.gameId)

    def eventStream(self, board, menuTable, mixer):
        while True:
            for event in self.client.board.stream_incoming_events():
                print(event)
                eventType = event['type']
                if eventType == 'gameStart':
                    self.gameId = event['game']['gameId']
                    if not event['game']['isMyTurn']: board.flip()
                    else: board.onlineTurn = True
                elif eventType == 'gameState':
                    if event['game']['isMyTurn']:
                        print("{1}'s time left: {0}".format(event['game']['secondsLeft'], event['game']['opponent']['username']))
                        c = board.storage.uciToCoords(event['game']['lastMove'])
                        m = board.tryMove(c[0], c[1], c[2])
                        if m: 
                            updateTable(menuTable)
                            board.onlineTurn = True
                            mixer.playMove(m[0], m[1])
                            if m[2]: guiButtons[1].enable()
                    else:
                        print("your time left: {0}".format(event['game']['secondsLeft']))
                elif eventType == 'chatLine':
                    print(event)
                else:
                    print("final", event)