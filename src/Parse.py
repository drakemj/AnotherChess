import chess
import chess.pgn

game1 = chess.Board()
print(game1)
nmove = chess.Move.from_uci("e2e4")
game1.push(nmove)
print(game1)
game1.pop()
print("hi")
print(game1)

class GameStack:
    game = chess.Board()

    def __init__(self):
        game = chess.Board()

    def pushMove(self, start, end, promote):
        s = "{0}{1}{2}{3}".format(chr(ord('a') + start[0]), start[1] + 1, chr(ord('a') + end[0]), end[1] + 1)
        print(s)
        move = chess.Move.from_uci(s)
        self.game.push(move)
        print(self.game)