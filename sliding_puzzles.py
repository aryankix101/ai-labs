import sys
import time


def print_puzzle(size, line):
    for i in range(len(line)):
        if i%size==0:
            line_str = line[i:i+size]
            line_list = []
            for c in line_str:
                line_list.append(c)
            print(' '.join(line_list))

def find_goal(size, board):
    goal_list = sorted(board)
    goal_list.remove('.')
    goal_list.append('.')
    goal_str = ''.join(goal_list)
    return(goal_str)
    #print_puzzle(size, goal_str)

def get_children(size, board):
    children = []
    space_idx = board.index('.')

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

    """for child in children:
        print_puzzle(size, child)
        print('-------------')"""
    
    return children


def goal_test(size, board):
    if board==find_goal(size, board):
        return True
    return False

def bfs(size, start_board):
    queue = [[start_board]]
    visited = set()
    while queue:
        path = queue.pop(0)
        board = path[-1]
        if goal_test(size, board):
            return len(path)-1
        
        elif board not in visited:
            for child in get_children(size, board):
                new_path = list(path)
                new_path.append(child)
                queue.append(new_path)

            visited.add(board)

def bfs_path(size, start_board):
    queue = [[start_board]]
    visited = set()
    while queue:
        path = queue.pop(0)
        board = path[-1]
        if goal_test(size, board):
            return path
        
        elif board not in visited:
            for child in get_children(size, board):
                new_path = list(path)
                new_path.append(child)
                queue.append(new_path)

            visited.add(board)

def hardest_puzzle(size, goal_board):
    queue = [goal_board]
    visited = set()
    check_furthest = []
    while queue:
        board = queue.pop(0)
        check_furthest.append(board)
        for child in get_children(size, board):
            if child not in visited:
                visited.add(child)
                queue.append(child)
    
    maximum = bfs(size, check_furthest[-1])
    max_list = [check_furthest[-1]]
    for board in check_furthest[len(check_furthest)-2::-1]:
        if bfs(size, board)==maximum:
            max_list.append(board)
        if bfs(size, board)<maximum:
            break
    
    for board in max_list:
        path = bfs_path(size, board)
        print("Start state: ")
        print_puzzle(size, board)
        print("Solution:")
        for b in path:
            print_puzzle(size, b)
            print('---------')
        print("Length: " + str(maximum))
        print()



with open('slide_puzzle_tests.txt') as f:
        for idx, line in enumerate(f):
            line_list = line.split()
            """print("Line " + str(idx) + " start state:")
            print_puzzle(int(line_list[0]), line_list[1])
            print("Line " + str(idx) + " goal state:")
            find_goal(int(line_list[0]), line_list[1])
            print("Line " + str(idx) + " children:")
            get_children(int(line_list[0]), line_list[1])"""
            """start = time.perf_counter()
            str_bfs = str(bfs(int(line_list[0]), line_list[1]))
            end = time.perf_counter()
            print("Line " + str(idx) + ": " + line_list[1] + ", " + str_bfs + " moves found in " + str(end-start) + " seconds")"""

print(hardest_puzzle(3, '12345678.'))
