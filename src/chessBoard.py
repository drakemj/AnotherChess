import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import math
import os


class ChessBoard:
    __EMPTY = 0
    __BLACK_KING = -1
    __BLACK_QUEEN = -2
    __BLACK_BISHOP = -3
    __BLACK_KNIGHT = -4
    __BLACK_ROOK = -5
    __BLACK_PAWN = -6
    __WHITE_KING = 1
    __WHITE_QUEEN = 2
    __WHITE_BISHOP = 3
    __WHITE_KNIGHT = 4
    __WHITE_ROOK = 5
    __WHITE_PAWN = 6

    def __init__(self, boardCellSize=81, coinSizeRatio=0.8, boardColor=([74, 139, 184], [111, 193, 227]),
                 coinColor=([21, 21, 21], [195, 223, 228])):
        self.__coinSizeRatio = coinSizeRatio
        self.__coinColor = coinColor
        self.__cellSize = boardCellSize
        self.__boardColor = boardColor
        self.__initializeBoard()
        self.__createBoard()
        self.__placePieces()

        # cv.imshow('frame', self.__boardImage.astype('uint8'))
        # cv.waitKey(0)
        # self.__boardImage.astype('uint8')

    def getBoardImage(self):
        return self.__boardImage.astype('uint8')

    def __initializeBoard(self):
        self.__board = np.zeros((8, 8), dtype='int') * self.__EMPTY
        self.__board[:, 1] = self.__WHITE_PAWN
        self.__board[0, 0] = self.__WHITE_ROOK
        self.__board[1, 0] = self.__WHITE_KNIGHT
        self.__board[2, 0] = self.__WHITE_BISHOP
        self.__board[3, 0] = self.__WHITE_QUEEN
        self.__board[4, 0] = self.__WHITE_KING
        self.__board[5:8, 0] = self.__board[0:3, 0][::-1]
        self.__board[:, 6:8] = -self.__board[:, 0:2][:, ::-1]
        # print(self.__board)
        # print("====================================")

    def __createBoard(self):
        cellSize = self.__cellSize
        boardColor = self.__boardColor

        self.__size = (cellSize * 8, cellSize * 8, 3)
        self.__boardImage = np.ones(self.__size, dtype='uint')
        for i in range(8):
            for j in range(8):
                if j % 2 == i % 2:
                    self.__boardImage[j * cellSize:(j + 1) * cellSize, i * cellSize:(i + 1) * cellSize] = boardColor[1]
                else:
                    self.__boardImage[j * cellSize:(j + 1) * cellSize, i * cellSize:(i + 1) * cellSize] = boardColor[0]

        self.__boardImage = self.__boardImage.reshape((cellSize * 8, cellSize * 8, -1))

        # cv.imshow("ChessBoard", self.__boardImage)
        # cv.waitKey(0)

    # Places pieces on the chess board as per the 2d array containing the information of the chess pieces
    def __placePieces(self):
        coinColor = self.__coinColor
        for i in range(8):
            for j in range(8):
                piece = self.__board[i, j]
                if piece != 0:
                    imgLoc = "ChessPieces" + os.sep + str(-abs(piece)) + ".png"
                    img = cv.imread(imgLoc, 0)
                    coinSize = int(self.__cellSize * self.__coinSizeRatio)
                    img_scaled = cv.resize(img, (coinSize, coinSize))
                    x, y = int((i + 0.5) * self.__cellSize - 0.5 * coinSize), int(
                        (j + 0.5) * self.__cellSize - 0.5 * coinSize)
                    for n in range(coinSize):
                        for m in range(coinSize):
                            if img_scaled[n, m] != 255:
                                color = coinColor[0]
                                if piece > 0:
                                    color = coinColor[1]
                                self.__boardImage[x + n, y + m] = color

    # Refresh the virtual chessboard
    # Is called whenever we want to update the virtual chessboard
    def refresh(self):
        self.__createBoard()
        self.__placePieces()
        # cv.imshow('frame', self.__boardImage.astype('uint8'))
        # cv.waitKey(0)
        return self.__boardImage.astype('uint8')

    # Function for moving the pieces on the chess board
    def movePiece(self, start, end):
        self.__board[end] = self.__board[start]
        self.__board[start] = self.__EMPTY
        # print(self.__board)
        # print("====================================")
