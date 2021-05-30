import sys
import time
from collections import deque  
import heapq

def goal_test(board):
    if board==find_goal(board):
        return True
    return False

def find_goal(board):
    return ''.join(sorted(board))[1:] + '.'

def print_puzzle(line):
    for i in range(len(line)):
        if i%size==0:
            line_str = line[i:i+size]
            line_list = []
            for c in line_str:
                line_list.append(c)
            print(' '.join(line_list))

def get_children(board):
    children = []
    space_idx = board.index('.')    
    size = int((len(board))**(1/2))
    if space_idx-size>=0:
        temp = []
        for c in board:
            temp.append(c)
        temp[space_idx], temp[space_idx-size] = temp[space_idx-size], temp[space_idx]
        children.append(''.join(temp))

    if space_idx+size<=len(board)-1:
        temp = []
        for c in board:
            temp.append(c)
        temp[space_idx], temp[space_idx+size] = temp[space_idx+size], temp[space_idx]
        children.append(''.join(temp))

    if (space_idx+1)%size!=0:
        if space_idx+1<=len(board)-1:
            temp = []
            for c in board:
                temp.append(c)
            temp[space_idx], temp[space_idx+1] = temp[space_idx+1], temp[space_idx]
            children.append(''.join(temp))

    if (space_idx)%size!=0:
        if space_idx-1>=0:
            temp = []
            for c in board:
                temp.append(c)
            temp[space_idx], temp[space_idx-1] = temp[space_idx-1], temp[space_idx]
            children.append(''.join(temp))

    return children

def parity_check(board):
    length = len(board)
    size = int((len(board))**(1/2))
    index = board.index('.')
    tempboard = board[:index] + board[index+1:]
    parity = 0
    for x in range(len(tempboard)-1):
        for y in range(x+1, len(tempboard)):
            if tempboard[x] > tempboard[y]:
                parity+=1
    
    if length%2!=0:
        if parity%2==0:
            return True
        else:
            return False
    else:
        blank_row = index//size
        if blank_row%2==0:
            if parity%2!=0:
                return True
            else:
                return False
        else:
            if parity%2==0:
                return True
            else:
                return False
    return None

def bfs(start_board):
    queue = deque([[start_board]])
    visited = set()
    while queue:
        path = queue.popleft()
        board = path[-1]
        if goal_test(board):
            return len(path)-1
        
        elif board not in visited:
            for child in get_children(board):
                new_path = list(path)
                new_path.append(child)
                queue.append(new_path)
            visited.add(board)

def k_dfs(start_state, k):
    fringe = [(start_state, 0, set(start_state))]
    while fringe:
        v = fringe.pop()
        if goal_test(v[0]):
            return v[1]
        if v[1] < k:
            for child in get_children(v[0]):
                if child not in v[2]:
                    temp_ancestors = v[2].copy()
                    temp_ancestors.add(child)
                    temp = (child, v[1]+1, temp_ancestors)
                    fringe.append(temp)
    return None

def id_dfs(start_state):
    max_depth = 0
    result = None
    while result is None:
        result = k_dfs(start_state, max_depth)
        max_depth+=1
    return result

def taxicab_distance(board):
    goal = find_goal(board)
    distance = 0
    size = int((len(board))**(1/2))
    for idx, c in enumerate(board):
        if c=='.':
            pass
        else:
            row, col = int(idx/size), idx%size
            idx_goal = goal.index(c)
            goal_row, goal_col = int(idx_goal/size), idx_goal%size
            distance += abs(row-goal_row) + abs(col-goal_col)
    return distance

def a_star(start_state):
    closed = set()
    fringe = [(taxicab_distance(start_state), start_state, 0)]
    heapq.heapify(fringe)
    while fringe:
        v = heapq.heappop(fringe)
        if goal_test(v[1]):
            return v[2]
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1]):
                if child not in closed:
                    temp_f = taxicab_distance(child) + (v[2]+1)
                    temp = (temp_f, child, v[2]+1) 
                    heapq.heappush(fringe, temp)
    return None

with open(sys.argv[1]) as f:
        for idx, line in enumerate(f):
            line_list = line.split()
            """start_parity = time.perf_counter()
            if parity_check(line_list[1])==False:
                end_parity=time.perf_counter()
                print("Line " + str(idx) + ": " + line_list[1] + ", no solution determined in " + str(end_parity-start_parity) + " seconds") 
            elif line_list[2]=='B':
                start_bfs = time.perf_counter()
                str_bfs = str(bfs(line_list[1]))
                end_bfs = time.perf_counter()
                print("Line " + str(idx) + ": " + line_list[1] + ", " + "BFS - " + str_bfs + " moves found in " + str(end_bfs-start_bfs) + " seconds")
            elif line_list[2]=='I':
                start_id_dfs = time.perf_counter()
                str_id_dfs = str(id_dfs(line_list[1]))
                end_id_dfs = time.perf_counter()
                print("Line " + str(idx) + ": " + line_list[1] + ", " + "ID-DFS - " + str_id_dfs + " moves found in " + str(end_id_dfs-start_id_dfs) + " seconds")
            elif line_list[2]=='A':
                start_astar = time.perf_counter()
                str_astar = str(a_star(line_list[1]))
                end_astar = time.perf_counter()
                print("Line " + str(idx) + ": " + line_list[1] + ", " + "A* - " + str_astar + " moves found in " + str(end_astar-start_astar) + " seconds")
            elif line_list[2]=='!':
                start_bfs = time.perf_counter()
                str_bfs = str(bfs(line_list[1]))
                end_bfs = time.perf_counter()
                print("Line " + str(idx) + ": " + line_list[1] + ", " + "BFS - " + str_bfs + " moves found in " + str(end_bfs-start_bfs) + " seconds")
                start_id_dfs = time.perf_counter()
                str_id_dfs = str(id_dfs(line_list[1]))
                end_id_dfs = time.perf_counter()
                print("Line " + str(idx) + ": " + line_list[1] + ", " + "ID-DFS - " + str_id_dfs + " moves found in " + str(end_id_dfs-start_id_dfs) + " seconds")
                start_astar = time.perf_counter()
                str_astar = str(a_star(line_list[1]))
                end_astar = time.perf_counter()
                print("Line " + str(idx) + ": " + line_list[1] + ", " + "A* - " + str_astar + " moves found in " + str(end_astar-start_astar) + " seconds")"""
            start_astar = time.perf_counter()
            str_astar = str(a_star(line.strip()))
            end_astar = time.perf_counter()
            print("Line " + str(idx) + ": " + line.strip() + ", " + "A* - " + str_astar + " moves found in " + str(end_astar-start_astar) + " seconds")
            print()