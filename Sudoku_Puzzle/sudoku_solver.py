import time
import random
import math
import sys


boards = []
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

    #print(global_list)
    constraints_dict = {}
    for i in range(n*n):
        value_set = set()
        for element in global_list:
            if i in element:
                for x in element:
                    if x!=i:
                        value_set.add(x)
        constraints_dict[i] = value_set
    
    # print(global_list)
    return constraints_dict

def count_instances(boards, symbol_set):
    dict_of_instances = {}
    for symbol in symbol_set:
        count = boards.count(symbol)
        dict_of_instances[symbol] = count
    return dict_of_instances

def goal_test(state):
    if '.' in state:
        return False
    return True

def get_next_unassigned_var(state):
    idx = state.find('.')
    return idx

def get_sorted_values(state, var, constraints_dict, symbol_set):
    idx_set = constraints_dict[var]
    value_set = set()
    for i in idx_set:
        value_set.add(state[i])
    temp_set = symbol_set-value_set
    #print(value_set)
    return temp_set

def csp_backtracking(state, constraints_dict, symbol_set):
    if goal_test(state): 
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var, constraints_dict, symbol_set):
        period = state[var]
        new_state = state[:var] + str(val) + state[var+1:]
        #print(new_state)
        result = csp_backtracking(new_state, constraints_dict, symbol_set)
        if result is not None:
            return result
    return None

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
    constraints_dict = create_constraint_sets(i[0], n, subblock_height, subblock_width)
    dict_of_instances = count_instances(i[0], symbol_set)
    solution = csp_backtracking(i[0], constraints_dict, symbol_set)
    print(solution)
    #print_function(solution)