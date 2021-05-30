import time
import random
import math
import sys
from collections import deque  

boards = []
call_count = 0
with open(sys.argv[1]) as f:
    for idx, line in enumerate(f):
        line_list = line.split()
        boards.append(line_list)

def print_function(boards):
    row_len = 0
    s = ''
    height = 0
    for i, val in enumerate(boards):
        if i==0:
            print('-----------------------')
        if height!=0:
            if subblock_height==height:
                print('-----------------------')
                height = 0
        if i%subblock_width==0:
            line_str = boards[i:i+subblock_width]
            line_list = []
            for c in line_str:
                line_list.append(c)
            s+=' '.join(line_list) + ' | '
            row_len += subblock_width
        if row_len==n:
            height+=1
            print(s)
            row_len = 0
            s = ''
    print()
    print()

def create_constraint_sets(boards, n, subblock_height, subblock_width):
    global_list = []
    idx_row = 0
    for i in range(len(boards)):
        if i%n==0:
            row_set = set()
            for i in range(i, i+n):
                row_set.add(i)
            global_list.append((row_set))
    
    temp_c_list = []
    for i in range(n):
        row_set = set()
        for row in global_list:
            sorted_row = sorted(row)
            temp = list(sorted_row)
            row_set.add(temp[i])
        temp_c_list.append((row_set))
    
    for col in temp_c_list:
        global_list.append(col)

    temp_first2_loops = []
    for i in range(n):
        if i%subblock_width==0:
            temp_first2_loops.append(i)
            temp = i
            for idx in range(subblock_width-1):
                temp = temp + n*subblock_height
                temp_first2_loops.append(temp)

    for i in temp_first2_loops:
        subblock_set = set()
        subblock_set.add(i)
        temp = i
        for idx_c in range(subblock_height):
            subblock_set.add(temp)
            temp_r = temp
            for idx_r in range(subblock_width-1):
                temp_r+=1
                subblock_set.add(temp_r)
            temp += n
        global_list.append((subblock_set))

    constraints_dict = {}
    for i in range(n*n):
        value_set = set()
        for element in global_list:
            if i in element:
                for x in element:
                    if x!=i:
                        value_set.add(x)
        constraints_dict[i] = value_set
    return constraints_dict, global_list

def goal_test(state):
    for check in state:
        if len(check)>1:
            return False
    return True

def get_sorted_values(state, var):
    return state[var]

def change_unknowns(board, symbol_set):
    new_board = []
    for c in board:
        if c=='.':
            temp_s = ''.join(symbol_set)
            new_board.append(temp_s)
        else:
            new_board.append(c)
    return new_board

def forward_looking(constraints_dict, changed_board, changed_indices):
    temp_board = changed_board.copy()
    queue = deque(changed_indices)
    if not changed_indices:
        list_of_solved = []
        for idx, c in enumerate(changed_board):
            if len(c)==1:
                list_of_solved.append(idx)
        queue = deque(list_of_solved)
    while queue:
        ele = queue.popleft()
        idx_set = constraints_dict[ele]
        for i in idx_set:
            change_str = changed_board[i]
            change_to = changed_board[ele]
            if change_str.find(change_to)!=-1:
                idx_of_replace = change_str.index(change_to)
                changed_board[i] = change_str[:idx_of_replace] + change_str[idx_of_replace+1:]
                if len(changed_board[i])==0:
                    return None, None
                if len(changed_board[i])==1:
                    queue.append(i)
    if changed_board!=temp_board:
        return changed_board, True
    else:
        return changed_board, False

def get_most_constrained_var(board):
    checking_list = []
    min_val = 999
    min_idx = 0
    for idx, x in enumerate(board):
        if len(x)>1:
            if len(x)<min_val:
                min_idx = idx
                min_val = len(x)
    return min_idx

def constraint_propagation(global_list, board):
    changed_indices = []
    """for idx, c in enumerate(board):
        if len(c)>1:
            for i in range(len(c)):
                idx_set = constraints_dict[idx]
                temp_list = []
                for x in idx_set:
                    for y in board[x]:
                        temp_list.append(y)
                if c[i] not in temp_list:
                    replacer = c[i]
                    board[idx] = replacer
                    changed_indices.append(idx)"""
    for tup in global_list:
        temp_list = []
        temp_list_2 = []
        indices = []
        for ele in tup:
            indices.append(ele)
            temp_list.append(board[ele])
            if len(board[ele])>1:
                for y in board[ele]:
                    temp_list_2.append(y)
            else:
                temp_list_2.append(board[ele])
            
        for idx, i in enumerate(temp_list):
            if len(i)>1:
                for c in i:
                    if temp_list_2.count(c)==1:
                        indice_to_change = indices[idx]
                        board[indice_to_change] = c
                        changed_indices.append(indices[idx])
                        break
                else:
                    continue
                break

        #or i in temp_list 
    #print(board, changed_indices)
    #print(changed_indices)
    return board, changed_indices              



def csp_backtracking_with_forward_looking(board, constraints_dict, symbol_set, global_list):
    global call_count
    call_count += 1
    if goal_test(board):
        return board
    var = get_most_constrained_var(board)
    for val in get_sorted_values(board, var):
        new_board = board.copy()
        new_board[var] = val
        checked_board, changes = forward_looking(constraints_dict, new_board, [var])
        if checked_board is not None:
            checked_board, solved_list = constraint_propagation(global_list, checked_board)
        while (checked_board is not None) and solved_list:
            #print(solved_list)
            checked_board, changes = forward_looking(constraints_dict, checked_board, solved_list)
            if checked_board is None:
                break
            checked_board, solved_list = constraint_propagation(global_list, checked_board)
        if checked_board is not None:
            result = csp_backtracking_with_forward_looking(checked_board, constraints_dict, symbol_set, global_list)
            if result is not None:
                return result
    return None

start = time.perf_counter()
for i in boards:
    #Calculating variables
    n = 0
    subblock_height = 0
    subblock_width = 0
    symbol_set = {}
    var_finder = i[0]
    n = math.sqrt(len(var_finder))
    temp_n_h = n
    subblock_height = math.floor(math.sqrt(temp_n_h))
    temp_n_w = n
    subblock_width = math.ceil(math.sqrt(temp_n_w))
    symbol_set = set()
    temp = n
    n = int(temp)
    for x in range(1, n+1):
        if x>9:
            break
        symbol_set.add(str(x))
    list_of_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    if n > 9:
        for l in range((n)-9):
            symbol_set.add(list_of_chars[l])
    #Solving
    constraints_dict, global_list = create_constraint_sets(i[0], n, subblock_height, subblock_width)
    changed_board = change_unknowns(i[0], symbol_set)
    possible_solution, changes = forward_looking(constraints_dict, changed_board, [])
    if possible_solution is not None:
        possible_solution, solved_list = constraint_propagation(global_list, possible_solution)
    while solved_list:
        possible_solution, changes = forward_looking(constraints_dict, possible_solution, solved_list)
        possible_solution, solved_list = constraint_propagation(global_list, possible_solution)
    
    solution = csp_backtracking_with_forward_looking(possible_solution, constraints_dict, symbol_set, global_list)
    print(''.join(solution))
    #print_function(''.join(solution))

end = time.perf_counter()   
#print(end-start)
#print(call_count)