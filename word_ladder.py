import sys
from collections import deque  
import time

start=time.perf_counter()
dict = {}

with open(sys.argv[1]) as f:
    line_list = [line.strip() for line in f]

with open(sys.argv[2]) as f:
    puzzle_list = [line.strip() for line in f]

def compare_strings(str1, str2):
    isTrue = False

    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            if isTrue:
                return False
            else:
                isTrue = True
    return isTrue

def create_graph():
    for idx, line in enumerate(line_list):
        list = []
        for restoflineA in line_list[idx+1:]:
            if compare_strings(line, restoflineA):
                list.append(restoflineA)
        for restoflineB in line_list[:idx]:
            if compare_strings(line, restoflineB):
                list.append(restoflineB)
        dict.update({line:list})

def shortest_path(start, end):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        vertex = path[-1]

        if vertex == end:
            return path

        elif vertex not in visited:
            for current_neighbour in dict.get(vertex):
                new_path = list(path)
                new_path.append(current_neighbour)
                queue.append(new_path)

            visited.add(vertex)

    return False

create_graph()
end = time.perf_counter()
print("Time to create the data structure was: " + str(end-start))
print("There are " + str(len(dict)) + " words in this dict.")

start2 = time.perf_counter()
for idx, line in enumerate(puzzle_list):
    line_split = line.split()
    print("Line: " + str(idx))
    if shortest_path(line_split[0], line_split[1])!=False:
        path = shortest_path(line_split[0], line_split[1])
        print("Length is: " + str(len(path)))
        for word in path:
            print(word)
    else:
        print("No Solution!")
    print()

end2 = time.perf_counter()
print("Time to solve all of these puzzles was: " + str(end2-start2))