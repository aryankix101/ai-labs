import time
import random
import math
import sys
from collections import deque  

board = sys.argv[1]
player = sys.argv[2]
boards = []
"""with open(sys.argv[3]) as f:
    for l in f:
        boards.append(l.rstrip())"""
opp_player = ''
if player=='x':
    opp_player='o'
else:
    opp_player='x'

def possible_moves(board, token):
    possible_moves = []
    indices_to_check = [index for index, char in enumerate(board) if char == opp_player]
    empty_spaces = set()
    for idx in indices_to_check:
        for space in find_empty_spaces(idx):
            empty_spaces.add(space)
    for space in empty_spaces:
        if is_valid(space):
            possible_moves.append(space)
    return possible_moves

def find_empty_spaces(idx):
    empty_spaces = []
    if idx%8==0:
        if (idx+1)<=len(board)-1: 
            if board[idx+1]=='.':
                empty_spaces.append((idx+1))
        if (idx-8)>=0:
            if board[idx-8]=='.':
                empty_spaces.append((idx-8))
        if (idx+8)<=len(board)-1:
            if board[idx+8]=='.':
                empty_spaces.append((idx+8))
    elif (idx+1)%8==0:
        if (idx-1)>=0:
            if board[idx-1]=='.':
                empty_spaces.append((idx-1))
        if (idx-8)>=0:
            if board[idx-8]=='.':
                empty_spaces.append((idx-8))
        if (idx+8)<=len(board)-1:
            if board[idx+8]=='.':
                empty_spaces.append((idx+8))
    else:
        if (idx+1)<=len(board)-1: 
            if board[idx+1]=='.':
                empty_spaces.append((idx+1))
        if (idx-1)>=0:
            if board[idx-1]=='.':
                empty_spaces.append((idx-1))
        if (idx-8)>=0:
            if board[idx-8]=='.':
                empty_spaces.append((idx-8))
        if (idx+8)<=len(board)-1:
            if board[idx+8]=='.':
                empty_spaces.append((idx+8))
        if (idx-7)>=0:
            if board[idx-7]=='.':
                empty_spaces.append((idx-7))
        if (idx+7)<=len(board)-1:
            if board[idx+7]=='.':
                empty_spaces.append((idx+7))
        if (idx-9)>=0:
            if board[idx-9]=='.':
                empty_spaces.append((idx-9))
        if (idx+9)<=len(board)-1:
            if board[idx+9]=='.':
                empty_spaces.append((idx+9))
    return empty_spaces

def is_valid(idx):
    has_iterated_1 = False
    temp_right = idx
    if ((temp_right+1)%8)!=0:
        temp_right = idx+1
    #temp_right = idx+1
    while temp_right<=len(board)-1 and temp_right>=0 and board[temp_right]!=player and board[temp_right]!='.' and ((temp_right+1)%8)!=0:
        temp_right+=1
        has_iterated_1 = True
    if (temp_right)<=len(board)-1 and (temp_right)>=0:
        if board[temp_right]==player and has_iterated_1:
            #print("Right " + str(idx))
            return True

    has_iterated_2 = False
    temp_left = idx
    if ((temp_left)%8)!=0:
        temp_left = idx-1
    while temp_left<=len(board)-1 and temp_left>=0 and board[temp_left]!=player and board[temp_left]!='.' and (temp_left%8)!=0:
        temp_left-=1
        has_iterated_2 = True
    if (temp_left)<=len(board)-1 and (temp_left)>=0:
        if board[temp_left]==player and has_iterated_2:
            #print("Left " + str(idx))
            return True

    has_iterated_3 = False
    temp_up = idx-8
    while temp_up<=len(board)-1 and temp_up>=0 and temp_up>7 and board[temp_up]!=player and board[temp_up]!='.':
        temp_up-=8
        has_iterated_3 = True
    if (temp_up)<=len(board)-1 and (temp_up)>=0:
        if board[temp_up]==player and has_iterated_3:
            #print("Up " + str(idx))
            return True

    has_iterated_4 = False
    temp_down = idx+8
    while temp_down<=len(board)-1 and temp_down>=0 and temp_down<56 and board[temp_down]!=player and board[temp_down]!='.':
        temp_down+=8
        has_iterated_4 = True
    if (temp_down)<=len(board)-1 and (temp_down)>=0:
        if board[temp_down]==player and has_iterated_4:
            #print("Down " + str(idx))
            return True
    
    has_iterated_5 = False
    temp_left_up = idx-9
    while temp_left_up<=len(board)-1 and temp_left_up>=0 and temp_left_up>7 and board[temp_left_up]!=player and board[temp_left_up]!='.' and (temp_left_up%8)!=0 and (idx%8)!=0:
        temp_left_up-=9
        has_iterated_5 = True
    if (temp_left_up)<=len(board)-1 and (temp_left_up)>=0:
        if board[temp_left_up]==player and has_iterated_5:
            #print("Left up " + str(idx))
            return True

    has_iterated_6 = False
    temp_right_up = idx-7
    while temp_right_up<=len(board)-1 and temp_right_up>=0 and temp_right_up>7 and board[temp_right_up]!=player and board[temp_right_up]!='.' and ((temp_right_up+1)%8)!=0 and (idx+1)%8!=0:
        temp_right_up-=7
        has_iterated_6 = True
    if (temp_right_up)<=len(board)-1 and (temp_right_up)>=0:
        if board[temp_right_up]==player and has_iterated_6:
            #print("Right up " + str(idx))
            print(idx, temp_right_up)
            return True

    temp_left_down = idx+7
    has_iterated_7 = False
    while temp_left_down<=len(board)-1 and temp_left_down>=0 and temp_left_down<56 and board[temp_left_down]!=player and board[temp_left_down]!='.' and (temp_left_down%8)!=0 and (idx%8)!=0:
        temp_left_down+=7
        has_iterated_7 = True
    if (temp_left_down)<=len(board)-1 and (temp_left_down)>=0:
        if board[temp_left_down]==player and has_iterated_7:
            #print("Left down " + str(idx))
            return True

    temp_right_down = idx+9
    has_iterated_8 = False
    while temp_right_down<=len(board)-1 and temp_right_down>=0 and temp_right_down<56 and board[temp_right_down]!=player and board[temp_right_down]!='.' and ((temp_right_down+1)%8)!=0 and ((idx+1)%8)!=0:
        temp_right_down+=9
        has_iterated_8 = True
    if (temp_right_down)<=len(board)-1 and (temp_right_down)>=0:
        if board[temp_right_down]==player and has_iterated_8:
            #print("Right down " + str(idx))
            print(idx, temp_right_down)
            return True

    return False
    
        
def move(board, token, move):
    to_change = set()
    idx = move

    has_iterated_1 = False
    temp_right = move+1
    temp_list_1 = []
    while temp_right<=len(board)-1 and temp_right>=0 and board[temp_right]!=player and board[temp_right]!='.' and ((temp_right-1)%8)!=0:
        temp_list_1.append(temp_right)
        temp_right+=1
        has_iterated_1 = True
    if (temp_right)<=len(board)-1 and (temp_right)>=0:
        if board[temp_right]==player and has_iterated_1:
            for idx in temp_list_1:
                to_change.add(idx)

    has_iterated_2 = False
    temp_left = move-1
    temp_list_2 = []
    while temp_left<=len(board)-1 and temp_left>=0 and board[temp_left]!=player and board[temp_left]!='.' and (temp_left%8)!=0:
        temp_list_2.append(temp_left)
        temp_left-=1
        has_iterated_2 = True
    if (temp_left)<=len(board)-1 and (temp_left)>=0:
        if board[temp_left]==player and has_iterated_2:
            for idx in temp_list_2:
                to_change.add(idx)
    
    has_iterated_3 = False
    temp_up = move-8
    temp_list_3 = []
    while temp_up<=len(board)-1 and temp_up>=0 and board[temp_up]!=player and board[temp_up]!='.':
        temp_list_3.append(temp_up)
        temp_up-=8
        has_iterated_3 = True
    if (temp_up)<=len(board)-1 and (temp_up)>=0:
        if board[temp_up]==player and has_iterated_3:
            for idx in temp_list_3:
                to_change.add(idx)

    has_iterated_4 = False
    temp_down = move+8
    temp_list_4 = []
    while temp_down<=len(board)-1 and temp_down>=0 and board[temp_down]!=player and board[temp_down]!='.':
        temp_list_4.append(temp_down)
        temp_down+=8
        has_iterated_4 = True
    if (temp_down)<=len(board)-1 and (temp_down)>=0:
        if board[temp_down]==player and has_iterated_4:
            for idx in temp_list_4:
                to_change.add(idx)
    
    has_iterated_5 = False
    temp_left_up = move-9
    temp_list_5 = []
    while temp_left_up<=len(board)-1 and temp_left_up>=0 and board[temp_left_up]!=player and board[temp_left_up]!='.' and (temp_left_up%8)!=0:
        temp_list_5.append(temp_left_up)
        temp_left_up-=9
        has_iterated_5 = True
    if (temp_left_up)<=len(board)-1 and (temp_left_up)>=0:
        if board[temp_left_up]==player and has_iterated_5:
            for idx in temp_list_5:
                to_change.add(idx)

    has_iterated_6 = False
    temp_right_up = move-7
    temp_list_6 = []
    while temp_right_up<=len(board)-1 and temp_right_up>=0 and board[temp_right_up]!=player and board[temp_right_up]!='.' and ((temp_right_up+1)%8)!=0:
        temp_list_6.append(temp_right_up)
        temp_right_up-=7
        has_iterated_6 = True
    if (temp_right_up)<=len(board)-1 and (temp_right_up)>=0:
        if board[temp_right_up]==player and has_iterated_6:
            for idx in temp_list_6:
                to_change.add(idx)

    has_iterated_7 = False
    temp_left_down = move+7
    temp_list_7 = []
    while temp_left_down<=len(board)-1 and temp_left_down>=0 and board[temp_left_down]!=player and board[temp_left_down]!='.' and (temp_left_down%8)!=0:
        temp_list_7.append(temp_left_down)
        temp_left_down+=7
        has_iterated_7 = True
    if (temp_left_down)<=len(board)-1 and (temp_left_down)>=0:
        if board[temp_left_down]==player and has_iterated_7:
            for idx in temp_list_7:
                to_change.add(idx)

    has_iterated_8 = False
    temp_right_down = move+9
    temp_list_8 = []
    while temp_right_down<=len(board)-1 and temp_right_down>=0 and board[temp_right_down]!=player and board[temp_right_down]!='.' and ((temp_right_down+1)%8)!=0:
        temp_list_8.append(temp_right_down)
        temp_right_down+=9
        has_iterated_8 = True
    if (temp_right_down)<=len(board)-1 and (temp_right_down)>=0:
        if board[temp_right_down]==player and has_iterated_8:
            for idx in temp_list_8:
                to_change.add(idx)
    
    temp_list = list(board)
    temp_list[move] = token
    for idx in to_change:
        temp_list[idx] = token
    
    updated_board = ''.join(temp_list)
    return updated_board

moves = possible_moves(board, player)
print(moves)
for idx, i in enumerate(moves):
    move_board = (move(board, player, i))
    print(move_board)
    """if move_board!=boards[idx]:
        print('Not correct')"""
