import berserk

with open('lichess.token') as f:
    token = f.read()

session = berserk.TokenSession(token)
client = berserk.Client(session)

board = client.board
for event in board.stream_incoming_events():
    print(event)
