class Board:
    board = [[0 for i in range(8)] for j in range(8)]
    whiteRook1 = False      #bools to keep track of castling rules
    whiteRook2 = False
    blackRook1 = False
    blackRook2 = False
    whiteKing = False
    blackKing = False
    heldPiece = 0
    turn = True
    flipped = False

    #notated columns, rows on the chessboard. (2, 3) is the third column, fourth row (from the bottom left)
    #1 - 6 are white pawns, rooks, knights, bishops, queens, and king, respectively. 11-16 are the same for black pieces.

    def __init__(self):
        for i in range(8):
            self.board[i][1] = 1
            self.board[i][6] = 11
            
            if i < 5:
                self.board[i][0] = i + 2
                self.board[i][7] = i + 12
            else:
                self.board[i][0] = 9 - i
                self.board[i][7] = 19 - i

    def debugBoard(self, b = board):
        for i in range(7, -1, -1):
            for j in range(8):
                print(b[j][i], end = '')
                if b[j][i]/10 < 1:
                    print(" ", end = '')
                print(" ", end = '')
            print()
        print()
                    
    def pickupPiece(self, pos):
        self.heldPiece = pos
        return self.board[pos[0]][pos[1]]

    def placePiece(self):
        self.heldPiece = 0
                    
    def inBounds(self, col, row):
        return col >= 0 and col < 8 and row >= 0 and row < 8

    def flip(self):
        self.flipped = not self.flipped

    def checkMove(self, start, end):
        if start == end:
            return False
        
        if self.turn:
            if self.board[start[0]][start[1]]/10 >= 1:
                return False
        else:
            if self.board[start[0]][start[1]]/10 < 1:
                return False

    def move(self, start, end):
        t = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = 0
        self.board[end[0]][end[1]] = t

    def isOccupied(self, col, row):         #returns 1 if enemy piece, 2 if friendly
        if self.board[col][row] == 0:
            return 0
        elif self.turn and self.board[col][row]/10 >= 1:
            return 1
        elif not self.turn and self.board[col][row]/10 < 1:
            return 1
        else:
            return 2
            
    def availableMoves(self, col, row, flip = False):
        out = [[0 for i in range(8)] for j in range(8)]
        p = self.board[col][row]
        if not flip:
            if self.turn and p > 10: return out
            if not self.turn and p < 10: return out
        else:
            self.turn = not self.turn
        piece = p % 10
        
        if piece == 1:        #PAWN
            direction = 1
            if not self.turn:
                direction = -1

            newRow = row + direction

            if self.inBounds(col, newRow) and not self.isOccupied(col, newRow):
                out[col][row+direction] = 1

            for i in (-1, 1):
                if self.inBounds(col + i, newRow) and self.isOccupied(col + i, newRow) == 1:
                    out[col+i][newRow] = 1

            if self.turn:
                if row == 1:
                    if not self.isOccupied(col, newRow + 1):
                        out[col][newRow + 1] = 1
            else:
                if row == 6:
                    if not self.isOccupied(col, newRow - 1):
                        out[col][newRow - 1] = 1
                            
        if piece == 2 or piece == 5:        #ROOK/QUEEN
            direction = [[col,row, i] for i in range(4)] #four directional checking
            while len(direction) > 0:
                for i in range(len(direction)):
                    d = direction[i]
                    if d[2] == 0:           #update checked square
                        d[1] += 1
                    elif d[2] == 1:
                        d[1] -= 1
                    elif d[2] == 2:
                        d[0] += 1
                    else:
                        d[0] -= 1

                    if not self.inBounds(d[0], d[1]) or self.isOccupied(d[0], d[1]) == 2:
                        direction.pop(i)
                        break
                    elif self.isOccupied(d[0], d[1]) == 1:
                        out[d[0]][d[1]] = 1
                        direction.pop(i)
                        break
                    else:
                        out[d[0]][d[1]] = 1

        if piece == 4 or piece == 5:        #BISHOP/QUEEN
            direction = [[col,row, i] for i in range(4)] #four directional checking
            while len(direction) > 0:
                for i in range(len(direction)):
                    d = direction[i]
                    if d[2] == 0:           #update checked square
                        d[0] += 1
                        d[1] += 1
                    elif d[2] == 1:
                        d[0] += 1
                        d[1] -= 1
                    elif d[2] == 2:
                        d[0] -= 1
                        d[1] += 1
                    else:
                        d[0] -= 1
                        d[1] -= 1

                    if not self.inBounds(d[0], d[1]) or self.isOccupied(d[0], d[1]) == 2:
                        direction.pop(i)
                        break
                    elif self.isOccupied(d[0], d[1]) == 1:
                        out[d[0]][d[1]] = 1
                        direction.pop(i)
                        break
                    else:
                        out[d[0]][d[1]] = 1

        if piece == 3:          #KNIFE
            o1 = [-1, 1]
            o2 = [-2, 2]

            for i in o1:
                for j in o2:
                    two =  [(col + i, row + j), (col + j, row + i)]
                    for p in two:
                        if not self.inBounds(p[0], p[1]) or self.isOccupied(p[0], p[1]) == 2:
                            continue
                        else:
                            out[p[0]][p[1]] = 1

        if piece == 6:          #KING
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    if i == 0 and j == 0 or not self.inBounds(col + i, row + j) or self.isOccupied(col + i, row + j) == 2:
                        continue
                    else:
                        out[col + i][row + j] = 1
        if flip:
            self.turn = not self.turn
        return out 

    def findKing(self):
        pos = 0
        for i in range(8):
                for j in range(8):
                    if self.turn and self.board[i][j] == 6:
                        pos = (i, j)
                        break
                    elif not self.turn and self.board[i][j] == 16:
                        pos = (i, j)
                        break
                if pos:
                    break
        return pos

    def inCheck(self, pos = 0, flip = False):
        o = []
        if flip: self.turn = not self.turn          # lol
        if not pos:
            pos = self.findKing()
        for i in range(8):
            for j in range(8):
                if self.turn and self.board[i][j] > 10:
                    if self.availableMoves(i, j, True)[pos[0]][pos[1]]:
                        o.append((i, j, self.board[i][j]))
                elif not self.turn and self.board[i][j] < 10:
                    if self.availableMoves(i, j, True)[pos[0]][pos[1]]:
                        o.append((i, j, self.board[i][j]))
        if flip: self.turn = not self.turn
        return o

    def moveInCheck(self, start, move):
        piece = self.board[move[0]][move[1]]
        self.move(start, move)
        out = self.inCheck()
        self.move(move, start)
        self.board[move[0]][move[1]] = piece
        return len(out)

    def isCheckmate(self):
        i = self.inCheck()
        
        if not len(i): return False

        pos = self.findKing()
        
        for x in range(-1, 2, 1):
            for y in range(-1, 2, 1):
                x1 = pos[0] + x
                y1 = pos[1] + y
                if (x or y) and self.inBounds(x1, y1):
                    if self.turn and self.board[x1][y1] < 10 or not self.turn and self.board[x1][y1] > 10:
                        continue
                    if not self.moveInCheck(pos, (x1, y1)): return False

        if len(i) == 2: return True

        counterAttackers = self.inCheck((i[0][0], i[0][1]), True)
        for ca in counterAttackers:
            if not self.moveInCheck((ca[0], ca[1]), (i[0][0], i[0][1])): return False
        if i[0][2] == 1 or i[0][2] == 3: return True

        xdir, ydir = 0, 0
        if pos[0] > i[0][0]: xdir = -1
        elif pos[0] < i[0][0]: xdir = 1
        if pos[1] > i[0][1]: ydir = -1
        elif pos[1] < i[0][1]: ydir = 1

        x, y = pos[0] + xdir, pos[1] + ydir
        while (x != i[0][0] or y != i[0][1]):
            defenders = self.inCheck((x, y), True)
            for d in defenders:
                if not self.moveInCheck((d[0], d[1]), (x, y)): return False

        return True