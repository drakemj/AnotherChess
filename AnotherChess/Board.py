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

    def isOccupied(self, col, row):
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
        
        if self.board[col][row] % 10 == 1:        #PAWN
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

        return out 