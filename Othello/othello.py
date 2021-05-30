#Notes:
"""count number of moves you have vs ur opponent, think about mobility, want to get corners, 
spaces next to corners low (spaces next to that high), count # of frontier pieces, rank victory even higher,
have an even distance from corners and prioritize having an even distance from edges next"""
#Notes pt 2:
"""my order is get corners, if you have the corner then get the three squares around it,
get safe edges, avoid moves that allow opponent to get to the corner, get any edge, play to middle, then play anything
"""
import time
import random
import math
import sys
from collections import deque  

def possible_moves(board, token):
    opp_player = ''
    if token=='x':
        opp_player='o'
    else:
        opp_player='x'
    possible_moves = []
    indices_to_check = [index for index, char in enumerate(board) if char==opp_player]
    empty_spaces = set()
    for idx in indices_to_check:
        for space in find_empty_spaces(idx, board):
            empty_spaces.add(space)
    for space in empty_spaces:
        if is_valid(space, board, token):
            possible_moves.append(space)
    return possible_moves

def find_empty_spaces(idx, board):
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

def is_valid(idx, board, player):
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
    while temp_left_up<=len(board)-1 and temp_left_up>=0 and temp_left_up>7 and board[temp_left_up]!=player and board[temp_left_up]!='.' and (temp_left_up%8)!=0  and (idx%8)!=0:
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
            return True

    return False
    
def move(board, player, move):
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
    temp_list[move] = player
    for idx in to_change:
        temp_list[idx] = player
    
    updated_board = ''.join(temp_list)
    return updated_board

def goal_test(board, player):
    if len(possible_moves(board, player))==0:
        return True
    return False

def check_score(board):
    #CHANGES: More overwhelming victories are weighted higher
    if goal_test(board, 'x') or goal_test(board, 'o'):
        score = 0
        if(goal_test(board, 'x')):
            score = 10000
        if(goal_test(board, 'o')):
            score = -10000
        score += board.count('x')-board.count('o')
        return score
    else:
        score = 0
        score += len(possible_moves(board, 'x'))-len(possible_moves(board, 'o'))
        corners = {0,7,56,63}
        for p in corners:
            if board[p]=='x':
                score+=100
            if board[p]=='o':
                score-=100
        d = {
            0: [1, 8, 9],
            7: [6, 14, 15],
            56: [48, 49, 57],
            63: [54, 55, 62]
        }
        x_corners=0
        o_corners=0
        x_near_empty_corner=0
        o_near_empty_corner=0
        for k in d:
            if board[k]=='x':
                for x in d[k]:
                    if board[x]=='x':
                        x_corners+=1
        for k in d:
            if board[k]=='o':
                for x in d[k]:
                    if board[x]=='o':
                        o_corners+=1
        for k in d:
            if board[k]=='.':
                for x in d[k]:
                    if board[x]=='x':
                        x_near_empty_corner+=1
        for k in d:
            if board[k]=='.':
                for x in d[k]:
                    if board[x]=='o':
                        o_near_empty_corner+=1
        score += 10 * x_corners
        score -= 10 * o_corners
        score -= 10 * x_near_empty_corner
        score += 10 * o_near_empty_corner
        return score

def max_step(board, depth, alpha, beta):
    if depth==0:
        return check_score(board)
    results = list()
    moves = possible_moves(board, 'x')
    for index in possible_moves(board, 'x'):
        next_board = move(board, 'x', index)
        val = min_step(next_board, depth-1, alpha, beta)
        #PRUNING
        alpha = max(alpha, val)
        results.append(val)
        if beta<=alpha:
            break
    if len(results)==0:
        return min_step(board, depth-1, alpha, beta)
    return max(results)

def min_step(board, depth, alpha, beta):
    if depth==0:
        return check_score(board)
    results = list()
    for index in possible_moves(board, 'o'):
        next_board = move(board, 'o', index)
        val = max_step(next_board, depth-1, alpha, beta)
        #PRUNING
        beta = min(beta, val)
        results.append(val)
        if beta<=alpha:
            break
    if len(results)==0:
        return max_step(board, depth-1, alpha, beta)
    return min(results)

def max_move(board, depth):
    list_of_vals = []
    list_of_boards = []
    moves = possible_moves(board, 'x')
    for idx, i in enumerate(moves):
        next_board = move(board, 'x', i)
        score = min_step(next_board, depth, -float('inf'), float('inf'))
        list_of_vals.append(score)
        list_of_boards.append(next_board)
    max_val = (max(list_of_vals))
    max_idx = list_of_vals.index(max_val)
    return moves[max_idx]

def min_move(board, depth):
    list_of_vals = []
    list_of_boards = []
    moves = possible_moves(board, 'o')
    for idx, i in enumerate(moves):
        next_board = move(board, 'o', i)
        score = max_step(next_board, depth, -float('inf'), float('inf'))
        list_of_vals.append(score)
        list_of_boards.append(next_board)
    min_val = (min(list_of_vals))
    min_idx = list_of_vals.index(min_val)
    return moves[min_idx]

def find_next_move(board, player, depth):
    if player=='x':
        return max_move(board, depth)
    else:
        return min_move(board, depth)


#For submitting to othello.tjhsst.edu
class Strategy():
   logging = True  # Optional
   def best_strategy(self, board, player, best_move, still_running):
       depth = 1
       for count in range(15):  # 15 is arbitrary; a depth that your code won't reach, but infinite loops crash the grader
           best_move.value = find_next_move(board, player, depth)
           depth += 1
           print(depth)

"""#For submitting to taking 75% or more of tokens
board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(15):  # 15 is arbitrary; a depth that your code won't reach, but infinite loops crash the grader
   print(find_next_move(board, player, depth))
   depth += 1"""