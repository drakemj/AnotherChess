import chess
import chess.pgn

class GameStack:
    game = chess.Board()

    def __init__(self):
        game = chess.Board()

    def pushMove(self, start, end, promote):
        select = ['q', 'r', 'n', 'b']
        s = "{0}{1}{2}{3}".format(chr(ord('a') + start[0]), start[1] + 1, chr(ord('a') + end[0]), end[1] + 1)
        if(promote != None): s += select[promote]
        move = chess.Move.from_uci(s)
        self.game.push(move)
        print(self.game)