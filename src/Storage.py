import chess
import chess.pgn

class GameStack:
    game = chess.Board()
    stack = []

    def __init__(self):
        self.game = chess.Board()
        self.stack = []

    def pushMove(self, start, end, promote):
        select = ['q', 'r', 'n', 'b']
        s = "{0}{1}{2}{3}".format(chr(ord('a') + start[0]), start[1] + 1, chr(ord('a') + end[0]), end[1] + 1)
        if(promote != None): s += select[promote]
        move = chess.Move.from_uci(s)
        self.game.push(move)

    def convertBoard(self, board):
        gameString = str(self.game)
        out = [[0 for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                c = gameString[(i*8 + j)*2]
                add = 0
                if c.islower(): add = 10
                c = c.lower()

                o = 0
                if c == 'p':
                    o = 1
                elif c == 'r':
                    o = 2
                elif c == 'n':
                    o = 3
                elif c == 'b':
                    o = 4
                elif c == 'q':
                    o = 5
                elif c == 'k':
                    o = 6
                out[j][7-i] = o + add

        return out

    def iterateBack(self):
        self.stack.append(self.game.pop())
        if len(self.game.move_stack): return False
        return True

    def iterateForward(self):
        self.game.push(self.stack.pop())
        if (len(self.stack)): return False
        return True
