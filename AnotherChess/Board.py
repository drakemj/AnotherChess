class Board:
    board = [[0 for i in range(8)] for j in range(8)]
    whiteRook1 = False      #bools to keep track of castling rules
    whiteRook2 = False
    blackRook1 = False
    blackRook2 = False
    whiteKing = False
    blackKing = False
    turn = True

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
        self.board[2][2] = 6

    def printBoard(self, b = board):
        for i in range(7, -1, -1):
            for j in range(8):
                print(b[j][i], end = '')
                if b[j][i]/10 < 1:
                    print(" ", end = '')
                print(" ", end = '')
            print()
                    
    def inBounds(self, col, row):
        return col >= 0 and col < 8 and row >= 0 and row < 8

    def checkMove(self, start, end):
        if start == end:
            return False
        
        if self.turn:
            if self.board[start[0]][start[1]]/10 >= 1:
                return False
        else:
            if self.board[start[0]][start[1]]/10 < 1:
                return False

    def isOccupied(self, col, row):         #returns 1 if enemy piece, 2 if friendly
        if self.board[col][row] == 0:
            return 0
        elif self.turn and self.board[col][row]/10 >= 1:
            return 1
        elif not self.turn and self.board[col][row]/10 < 1:
            return 1
        else:
            return 2
            
    def availableMoves(self, col, row):
        out = [[0 for i in range(8)] for j in range(8)]
        piece = self.board[col][row] % 10
        
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
            direction = [[row,col, i] for i in range(4)] #four directional checking
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
            direction = [[row,col, i] for i in range(4)] #four directional checking
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

        return out 