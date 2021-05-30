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