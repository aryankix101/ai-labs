import sys
import time
from collections import deque  


def goal_test(board):
    if board==find_goal(board):
        return True
    return False

def find_goal(board):
    return ''.join(sorted(board))[1:] + '.'

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


def bfs(size, start_board):
    queue = deque([[start_board]])
    visited = set()
    while queue:
        path = queue.popleft()
        board = path[-1]
        if goal_test(board):
            return len(path)-1
        
        elif board not in visited:
            for child in get_children(size, board):
                new_path = list(path)
                new_path.append(child)
                queue.append(new_path)

            visited.add(board)

def bibfs(size, start_board):
    fringe_start = deque()
    visited_start = set()
    fringe_start.append((start_board, 0))
    visited_start.add(start)
    fringe_end = deque()
    visited_end = set()
    fringe_end.append((find_goal(start_board), 0))
    visited_end.add(find_goal(start_board))
    while fringe_start and fringe_end:
        if fringe_start:
            v = fringe_start.popleft()
            isTrue = False
            correct_fringe = ()
            for x in fringe_end:
                for y in x:
                    if v[0]==y:
                        isTrue = True
                        correct_fringe = x
                        break
            if isTrue:
                return v[1] + correct_fringe[1]
            for child in get_children(size, v[0]):
                if child not in visited_start:
                    fringe_start.append((child, v[1]+1))
                    visited_start.add(child)
        if fringe_end:
            l = fringe_end.popleft()
            isTrue = False
            correct_fringe = ()
            for x in fringe_start:
                for y in x:
                    if l[0]==y:
                        isTrue = True
                        correct_fringe = x
                        break
            if isTrue:
                return l[1] + correct_fringe[1]
            for child in get_children(size, l[0]):
                if child not in visited_end:
                    fringe_end.append((child, l[1]+1))
                    visited_end.add(child)
    return None

with open(sys.argv[1]) as f:
        for idx, line in enumerate(f):
            line_list = line.split()
            start = time.perf_counter()
            str_bfs = str(bfs(int(line_list[0]), line_list[1]))
            end = time.perf_counter()
            print("Line " + str(idx) + ": " + line_list[1] + ", " + str_bfs + " moves found in " + str(end-start) + " seconds (using bfs)")
            start2 = time.perf_counter()
            str_bibfs = str(bibfs(int(line_list[0]), line_list[1]))
            end2 = time.perf_counter()
            print("Line " + str(idx) + ": " + line_list[1] + ", " + str_bibfs + " moves found in " + str(end2-start2) + " seconds (using bi-bfs)")