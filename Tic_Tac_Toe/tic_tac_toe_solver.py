import time
import random
import math
import sys
from collections import deque

def game_over(board):
    #print(board)
    if board[0]==board[1]==board[2] and board[0]!='.':
        return True, board[0]
    if board[3]==board[4]==board[5] and board[3]!='.':
        return True, board[3]
    if board[6]==board[7]==board[8] and board[6]!='.':
        return True, board[6]
    if board[0]==board[4]==board[8] and board[0]!='.':
        return True, board[0]
    if board[2]==board[4]==board[6] and board[2]!='.':
        return True, board[2]
    if board[0]==board[3]==board[6] and board[0]!='.':
        return True, board[0]
    if board[1]==board[4]==board[7] and board[1]!='.':
        return True, board[1]
    if board[2]==board[5]==board[8] and board[2]!='.':
        return True, board[2]
    if '.' not in board:
        #print('draw')
        return True, 'draw'
    return False, None

def possible_next_boards(board, current_player):
    list_of_boards = []
    for idx, c in enumerate(board):
        if c=='.':
            tempo = board
            temp_board = tempo[:idx] + current_player + tempo[idx+1:]
            list_of_boards.append(temp_board)
    return list_of_boards

def max_step(board):
    isTrue, who_won= game_over(board)
    if computer=='X':
        if isTrue:
            if who_won==computer:
                return 1
            if who_won=='draw':
                return 0
            if who_won!=computer:
                return -1
    else:
        if isTrue:
            if who_won==computer:
                return -1
            if who_won=='draw':
                return 0
            if who_won!=computer:
                return 1
    results = list()
    if board.count('X')==board.count('O'):
        for next_board in possible_next_boards(board, 'X'):
            results.append(min_step(next_board))
    else:
        for next_board in possible_next_boards(board, 'O'):
            results.append(min_step(next_board))
    return max(results)

def min_step(board):
    isTrue, who_won= game_over(board)
    if computer=='X':
        if isTrue:
            if who_won==computer:
                return 1
            if who_won=='draw':
                return 0
            if who_won!=computer:
                return -1
    else:
        if isTrue:
            if who_won==computer:
                return -1
            if who_won=='draw':
                return 0
            if who_won!=computer:
                return 1
    results = list()
    if board.count('X')==board.count('O'):
        for next_board in possible_next_boards(board, 'X'):
            results.append(max_step(next_board))
    else:
        for next_board in possible_next_boards(board, 'O'):
            results.append(max_step(next_board))
    return min(results)

def max_move(board):
    list_of_vals = []
    list_of_boards = []
    list_of_indices = []
    for next_board in possible_next_boards(board, 'X'):
        num = min_step(next_board)
        idx = [i for i in range(len(board)) if board[i] != next_board[i]]
        idx_str = str(idx[0])
        if num==-1:
            print("Moving at " + idx_str + " results in a loss.")
            list_of_vals.append(-1)
            list_of_indices.append(-1)
            list_of_boards.append(next_board)
        if num==0:
            print("Moving at " + idx_str + " results in a tie.")
            list_of_vals.append(0)
            list_of_indices.append(0)
            list_of_boards.append(next_board)
        if num==1:
            print("Moving at " + idx_str + " results in a win.")
            list_of_vals.append(1)
            list_of_indices.append(1)
            list_of_boards.append(next_board)
    index_to_choose = list_of_indices.index(max(list_of_vals))
    return list_of_boards[index_to_choose]


def min_move(board):
    list_of_vals = []
    list_of_boards = []
    list_of_indices = []
    for next_board in possible_next_boards(board, 'O'):
        num = max_step(next_board)
        idx = [i for i in range(len(board)) if board[i] != next_board[i]]
        idx_str = str(idx[0])
        if num==1:
            print("Moving at " + idx_str + " results in a loss.")
            list_of_vals.append(1)
            list_of_indices.append(1)
            list_of_boards.append(next_board)
        if num==0:
            print("Moving at " + idx_str + " results in a tie.")
            list_of_vals.append(0)
            list_of_indices.append(0)
            list_of_boards.append(next_board)
        if num==-1:
            print("Moving at " + idx_str + " results in a win.")
            list_of_vals.append(-1)
            list_of_indices.append(-1)
            list_of_boards.append(next_board)
    index_to_choose = list_of_indices.index(min(list_of_vals))
    return list_of_boards[index_to_choose]

def print_board(board):
    print(board[0:3] + '  012')
    print(board[3:6] + '  345')
    print(board[6:9] + '  678')

board = sys.argv[1]
computer = ''
opp_computer = ''
if board=='.........':
    print('Should I be X or O?')
    inp = input()
    computer = inp
    if computer=='X':
        opp_computer='O'
    else:
        opp_computer='X'
else:
    if board.count('X')==board.count('O'):
        computer = 'X'
        opp_computer = 'O'
    else:
        computer = 'O'
        opp_computer = 'X'

if computer=='X':
    isTrue, who_won = game_over(board)
    print()
    print("Current board: ")
    print_board(board)
    print()
    while isTrue==False:
        new_board = max_move(board)
        idx = [i for i in range(len(board)) if board[i] != new_board[i]]
        idx_str = str(idx[0])
        print()
        print("I choose space " + idx_str + '.')
        print()
        isTrue, who_won = game_over(new_board)
        board = new_board
        print("Current board: ")
        print_board(board)
        print()
        if isTrue==True:
            break
        idx_avail = [str(i) for i in range(len(board)) if board[i]=='.']
        print("You can move to any of these spaces: " + ', '.join(idx_avail) + '.')
        print("Your choice?")
        inp = input()
        int_inp = int(inp)
        temp_board = board
        board = temp_board[:int_inp] + 'O' + temp_board[int_inp+1:]
        print()
        print("Current board: ")
        print_board(board)
        print()
        isTrue, who_won = game_over(board)
    isTrue, who_won = game_over(board)
    if who_won==computer:
        print("I win!")
    if who_won==opp_computer:
        print("You win!")
    if who_won=='draw':
        print("We tied!")
        
else:
    isTrue, who_won = game_over(board)
    print()
    print("Current board: ")
    print_board(board)
    print()
    if board=='.........':
        while isTrue==False:
            idx_avail = [str(i) for i in range(len(board)) if board[i]=='.']
            print("You can move to any of these spaces: " + ', '.join(idx_avail) + '.')
            print("Your choice?")
            inp = input()
            int_inp = int(inp)
            temp_board = board
            board = temp_board[:int_inp] + 'X' + temp_board[int_inp+1:]
            print()
            print("Current board: ")
            print_board(board)
            print()
            isTrue, who_won = game_over(board)
            if isTrue==True:
                break
            new_board = min_move(board)
            idx = [i for i in range(len(board)) if board[i] != new_board[i]]
            idx_str = str(idx[0])
            print()
            print("I choose space " + idx_str + '.')
            print()
            isTrue, who_won = game_over(new_board)
            board = new_board
            print("Current board: ")
            print_board(board)
            print()
    else:
        while isTrue==False:
            new_board = min_move(board)
            idx = [i for i in range(len(board)) if board[i] != new_board[i]]
            idx_str = str(idx[0])
            print()
            print("I choose space " + idx_str + '.')
            print()
            isTrue, who_won = game_over(new_board)
            board = new_board
            print("Current board: ")
            print_board(board)
            print()
            if isTrue==True:
                break
            idx_avail = [str(i) for i in range(len(board)) if board[i]=='.']
            print("You can move to any of these spaces: " + ', '.join(idx_avail) + '.')
            print("Your choice?")
            inp = input()
            int_inp = int(inp)
            temp_board = board
            board = temp_board[:int_inp] + 'X' + temp_board[int_inp+1:]
            print()
            print("Current board: ")
            print_board(board)
            print()
            isTrue, who_won = game_over(board)
        
    isTrue, who_won = game_over(board)
    if who_won==computer:
        print("I win!")
    if who_won==opp_computer:
        print("You win!")
    if who_won=='draw':
        print("We tied!")