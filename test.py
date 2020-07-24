def bfs(start, end):
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