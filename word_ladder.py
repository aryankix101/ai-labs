import sys, time

start=time.time()
file = open(sys.argv[1], "r")
lines = file.readlines()
dict = {}

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
    for idx, line in enumerate(lines):
        list = []
        for restoflineA in lines[idx+1:]:
            if compare_strings(line, restoflineA):
                list.append(restoflineA.strip('\n'))
        for restoflineB in lines[:idx]:
            if compare_strings(line, restoflineB):
                list.append(restoflineB.strip('\n'))
        dict.update({line.strip('\n'):list})

def degree_distribution():
    maxsize = max([len(v) for v in dict.values()])
    list = [0] * (maxsize+1)
    for i in range(maxsize+1):
        for v in dict.values():
            if len(v)==i:
                list[i]+=1
    return ' '.join(map(str, list))

def edge_count():
    return sum([len(v) for v in dict.values()])//2

def get_second_degree():
    remove_zeroes = degree_distribution().split()
    remove_zeroes = [i for i in remove_zeroes if i != 0]
    degree = (len(remove_zeroes))-2
    for k in dict.keys():
        if len(dict.get(k))==degree:
            return k

def get_numofcomponentsizes():
    visited = set()
    sizes = set()
    for node in dict.keys():
        if node not in visited:
            visited.add(node)

            component = []
            queue = []
            queue.append(node)

            while queue:
                node = queue.pop(0)
                component.append(node)
                for neighbor in dict.get(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            sizes.add(len(component))
    return len(sizes)

def largest_componentsize():
    visited = set()
    sizes = set()
    for node in dict.keys():
        if node not in visited:
            visited.add(node)

            component = []
            queue = []
            queue.append(node)

            while queue:
                node = queue.pop(0)
                component.append(node)
                for neighbor in dict.get(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            sizes.add(len(component))
    return max(sizes)

def get_k2():
    visited = set()
    sizes = []
    for node in dict.keys():
        if node not in visited:
            visited.add(node)

            component = []
            queue = []
            queue.append(node)

            while queue:
                node = queue.pop(0)
                component.append(node)
                for neighbor in dict.get(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            if len(component)==2:
                sizes.append(component)
    return len(sizes)

def get_k3():
    visited = set()
    sizes = []
    for node in dict.keys():
        if node not in visited:
            visited.add(node)

            component = []
            queue = []
            queue.append(node)

            while queue:
                node = queue.pop(0)
                component.append(node)
                for neighbor in dict.get(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            if len(component)==3:
                temp = []
                for i, vertex in enumerate(component):
                    for vertex_compare in component[i+1:]:
                        if compare_strings(vertex, vertex_compare):
                            temp.append(True)
                        else:
                            temp.append(False)
                if all(temp):
                    sizes.append(component)
    return len(sizes)

def get_k4():
    visited = set()
    sizes = []
    for node in dict.keys():
        if node not in visited:
            visited.add(node)

            component = []
            queue = []
            queue.append(node)

            while queue:
                node = queue.pop(0)
                component.append(node)
                for neighbor in dict.get(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            if len(component)==4:
                temp = []
                for i, vertex in enumerate(component):
                    for vertex_compare in component[i+1:]:
                        if compare_strings(vertex, vertex_compare):
                            temp.append(True)
                        else:
                            temp.append(False)
                if all(temp):
                    sizes.append(component)
    return len(sizes)

def get_neighbours(input_word):
    return dict.get(input_word)

def furthest(input_word):
    visited = []
    queue = []
    check_furthest = []
    visited.append(input_word)
    queue.append(input_word)
    while queue:
        popped = queue.pop(0)
        check_furthest.append(popped)
        for v in dict.get(popped):
            if v not in visited:
                visited.append(v)
                queue.append(v)
    return check_furthest[-1]

def shortest_path(start, end):
    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        vertex = path[-1]

        if vertex == end:
            return path

        elif vertex not in visited:
            for current_neighbour in dict.get(vertex):
                new_path = list(path)
                new_path.append(current_neighbour)
                queue.append(new_path)

            visited.add(vertex)
                

def print4():
    print("Word count: " + str(len(dict)))
    print("Edge count: " + str(edge_count()))
    print("Degree list: " + degree_distribution())
    print("Construction time: " + str(round((time.time()-start), 1)) +"s")

def printrest():
    print("Second degree word: " + get_second_degree())
    print("Connected component size count: " + str(get_numofcomponentsizes()))
    print("Largest component size: " + str(largest_componentsize()))
    print("K2 count: " + str(get_k2()))
    print("K3 count: " + str(get_k3()))
    print("K4 count: " + str(get_k4()))
    print("Neighbors: " + str(get_neighbours(sys.argv[2])))
    print("Farthest: " + furthest(sys.argv[2]))
    print("Path: " + str(shortest_path(sys.argv[2], sys.argv[3])))
    print("Construction time: " + str(round((time.time()-start), 1)) +"s")

if __name__ == '__main__':
    create_graph()
    if len(sys.argv)==2:
        print4()
    else:
        printrest()