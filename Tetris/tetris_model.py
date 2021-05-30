"""
height, width, list of number of blocks in each index
"""

import math
import sys

board = list(sys.argv[1])
board_str = (sys.argv[1])
board_list = []
while len(board_list)!=20:
    board_list.append(board[0:10])
    del board[0:10]
#All piece orientations
piece_I_orient0 = [['#', "#", "#", "#"]]
piece_I_orient1 = [["#"],
                   ["#"],
                   ["#"],
                   ["#"]]
piece_O = [["#", "#"],
           ["#", "#"]]
piece_T_orient0 = [[" ", "#", " "],
                   ["#", "#", "#"]]
piece_T_orient1 = [["#", " "],
                   ["#", "#"],
                   ["#", " "]]
piece_T_orient2 = [["#", "#", "#"],
                   [" ", "#", " "]]
piece_T_orient3 = [[" ", "#"],
                   ["#", "#"],
                   [" ", "#"]]
piece_S_orient0 = [[" ", "#", "#"],
                   ["#", "#", " "]]
piece_S_orient1 = [["#", " "],
                   ["#", "#"],
                   [" ", "#"]]
piece_Z_orient0 = [["#", "#", " "],
                   [" ", "#", "#"]]
piece_Z_orient1 = [[" ", "#"],
                   ["#", "#"],
                   ["#", " "]]
piece_J_orient0 = [["#", " ", " "],
                   ["#", "#", "#"]]
piece_J_orient1 = [["#", "#"],
                   ["#", " "],
                   ["#", " "]]
piece_J_orient2 = [["#", "#", "#"],
                   [" ", " ", "#"]]
piece_J_orient3 = [[" ", "#"],
                   [" ", "#"],
                   ["#", "#"]]
pieces = [piece_I_orient1, piece_I_orient1, piece_O, piece_T_orient0, piece_T_orient1, piece_T_orient2, piece_T_orient3, piece_S_orient0, piece_S_orient1, piece_Z_orient0, piece_Z_orient1, piece_J_orient0, piece_J_orient1, piece_J_orient2, piece_J_orient3]

def print_puzzle(board,num_rows,num_cols):
    count = 0
    for i in range(num_rows):
        for x in range(num_cols):
            print(board_str[count] + "  ", end = "")
            count+=1
        print("")
print_puzzle(board, 20, 10)     
#print(board_list)

def check_update_rows(board):
    count = 0
    for i, r in enumerate(board):
        if ' ' not in r:
            board.pop(i)
            count+=1
    for i in range(count):
        board.insert(0, [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def find_row_indexes(maxLengthRow, board):
    length_of_row = len(board[0])
    look = []
    for i in range(length_of_row):
        if i+maxLengthRow<=length_of_row-1:
            t_list = []
            for i in range(i, i+maxLengthRow):
                t_list.append(i)
            look.append(t_list)
    return look

def find_col_indexes(maxLengthCol, board):
    length_of_col = len(board)
    look = []
    for i in range(length_of_col):
        if i+maxLengthCol<=length_of_col-1:
            t_list = []
            for i in range(i, i+maxLengthCol):
                t_list.append(i)
            look.append(t_list)
    return look

#Place piece returns list of strings (each string represents a board state)
def place_piece(piece, board):
    piece_orientations = []
    maxList = max(piece, key = len)
    maxLengthRow = max(map(len, piece))
    maxLengthCol = len(piece)
    row_indexes = find_row_indexes(maxLengthRow, board)
    col_indexes = find_col_indexes(maxLengthCol, board)
    print(row_indexes, col_indexes)
    for h_section in row_indexes:
        for v_section in col_indexes:
            for partial_row_idx in v_section:
                for partial_col_idx in h_section:
                    t_row = board[partial_row_idx]
                    t_row[partial_col_idx]

        
#print(board_list)
text_file = open("tetrisout.txt", "w")
for piece in pieces:
    list_of_placements = place_piece(piece, board_list)
    for placement in list_of_placements:
        text_file.write(placement)
text_file.close()