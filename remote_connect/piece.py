#军棋规则

import random

# class chess_board():
#     def __init__(self):
#         self.board = [[0 for i in range(9)] for j in range(10]
#         self.red = []
#         self.black = []
#         self.init_board()

#     def init_board(self):
#         for i in range(9):
#             self.board[0][i] = chess_piece("p", "red", i, 0)
#             self.board[9][i] = chess_piece("p", "black", i, 9)
#             self.red.append(self.board[0][i])
#             self.black.append(self.board[9][i])
#         self.board[2][1] = chess_piece("m", "red", 1, 2)
#         self.board[2][7] = chess_piece("m", "red", 7, 2)
#         self.board[7][1] = chess_piece("m", "black", 1, 7)
#         self.board[7][7] = chess_piece("m", "black", 7, 7)
#         self.red.append(self.board[2][1])
#         self.red.append(self.board[2][7])
#         self.black.append(self.board[7][1])
#         self.black.append(self.board[7][7])
#         self.board[0][1] = chess_piece("c", "red", 1, 0)
#         self.board[0][7] = chess_piece("c", "red", 7, 0)
#         self.board[9][1] = chess_piece("c", "black", 1, 9)
#         self.board[9][7] = chess_piece("c", "black", 7, 9)
#         self.red.append(self.board[0][1])
#         self.red.append(self.board[0][7])
#         self.black.append(self.board[9][1])
#         self.black.append(self.board[9][7])
#         self.board[0][2] = chess_piece("x", "red", 2, 0)
#         self.board[0][6] = chess_piece("x", "red", 6, 0)
#         self.board[9][2] = chess_piece("x", "black", 2, 9)
#         self.board[9][6] = chess_piece("x", "black", 6, 9)
#         self.red.append(self.board[0][2])
#         self

class chess_piece():
    def __init__(self, name, color, x, y, alive):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.alive = alive

    def move(self, x, y):
        self.x = x
        self.y = y

    def die(self):
        self.alive = False
