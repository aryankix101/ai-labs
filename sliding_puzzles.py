import sys
import time


def find_goal(size, board):
    goal_list = sorted(board)
    goal_list.remove('.')
    goal_list.append('.')
    goal_str = ''.join(goal_list)
    return(goal_str)

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

with open(sys.argv[1]) as f:
        for idx, line in enumerate(f):
            line_list = line.split()
            start = time.perf_counter()
            str_bfs = str(bfs(int(line_list[0]), line_list[1]))
            end = time.perf_counter()
            print("Line " + str(idx) + ": " + line_list[1] + ", " + str_bfs + " moves found in " + str(end-start) + " seconds")