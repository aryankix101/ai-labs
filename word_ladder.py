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

def singeltons():
    count = 0
    for v in dict.values():
        if len(v)==0:
            count+=1
    return count

def largest_componentsize():
    visited = set()
    sizes = set()
    for node in dict.keys():
        if node not in visited:
            visited.add(node)

            component = []
            queue = deque()
            queue.append(node)

            while queue:
                node = queue.popleft()
                component.append(node)
                for neighbor in dict.get(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            sizes.add(len(component))
    return max(sizes)

def get_largest_component():
    maxsize = largest_componentsize()
    visited = set()
    components = []
    dict2 = {}
    for node in dict.keys():
        if node not in visited:
            visited.add(node)

            component = []
            queue = deque()
            queue.append(node)

            while queue:
                node = queue.popleft()
                component.append(node)
                for neighbor in dict.get(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            components.append(component)
            if len(component)==maxsize:
                dict_temp = {node: component}
                dict2.update(dict_temp)  
                break 

    return dict2


def diff_components():
    maxsize = max([len(v) for v in dict.values()])
    components = set()
    for i in range(1, maxsize+1):
        for v in dict.values():
            if len(v) not in components:
                components.add(len(v))
    return len(components)

def find_path(start, end):
    queue = deque([[start]])
    visited = set()
    while queue:
        path = queue.popleft()
        word = path[-1]
        if word==end:
            return path

        elif word not in visited:
            for child in dict.get(word):
                new_path = list(path)
                new_path.append(child)
                queue.append(new_path)

            visited.add(word)

def furthest():
    dict_largest = get_largest_component()
    key = list(dict_largest.keys())[0]
    queue = deque([key])
    visited = [key]
    check_furthest = []
    while queue:
        word = queue.popleft()
        check_furthest.append(word)
        for child in dict.get(word):
            if child not in visited:
                visited.append(child)
                queue.append(child)

    print("Longest ideal path is between " + key + " and " + check_furthest[-1])
    print("Solution:")
    path = find_path(key, check_furthest[-1])
    for word in path:
        print(word)
    print("Length of longest ideal path: " + str(len(path)))

create_graph()
end = time.perf_counter()
print("Time to create the data structure was: " + str(end-start))
print("There are " + str(len(dict)) + " words in this dict.")

"""start2 = time.perf_counter()
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
print("Time to solve all of these puzzles was: " + str(end2-start2))"""

print("Number of singletons: " + str(singeltons()))
print("Largest connected subcomponent size: " + str(largest_componentsize()))
print("Total subcomponents (exlcuding singletons): " + str(diff_components()))
print(furthest())