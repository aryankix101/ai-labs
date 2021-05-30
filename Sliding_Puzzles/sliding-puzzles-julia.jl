using Printf

function goal_test(board)
    if board==find_goal(board)
        return true
    end
    return false
end

function find_goal(board)
    temp_joined_board = join(sort(board))
    return_board = temp_joined_board[1:end] * "."
    return return_board
end

function get_children(size,board)
    children = []
    space_idx = findfirst(".", board)

    if space_idx-size>=0
        temp = []
        for c in board
            push!(temp, c)
        end
        temp[space_idx], temp[space_idx-size] = temp[space_idx-size], temp[space_idx]
        push!(children, join(temp))
    end

    if space_idx+size<=length(board)-1
        temp = []
        for c in board
            push!(temp, c)
        end
        temp[space_idx], temp[space_idx+size] = temp[space_idx+size], temp[space_idx]
        push!(children, join(temp))
    end

    if mod(space_idx+1, size)!=0
        if space_idx+1<=length(board)-1
            temp = []
            for c in board
                push!(temp, c)
            end
            temp[space_idx], temp[space_idx+1] = temp[space_idx+1], temp[space_idx]
            push!(children, join(temp))
        end
    end

    if mod(space_idx, size)!=0
        if space_idx-1>=0
            temp = []
            for c in board
                push!(temp, c)
            end
            temp[space_idx], temp[space_idx-1] = temp[space_idx-1], temp[space_idx]
            push!(children, join(temp))
        end
    end

    return children
end
    
function bfs(size, start_board)
    queue = Deque([[start_board]])
    visited = Set()
    while .!(isempty(queue))
        path = popfirst!(queue)
        board = path[end]
        if goal_test(board)
            return length(path)-1
        
        elseif .!(occursin(board, visited))
            for child in get_children(size, board)
                new_path = convert(Array, path)
                push!(new_path, child)
                push!(queue, new_path)
            end
        end
            push!(visited, board)
    end
end

open("slide_puzzle_test.txt", "r") do f
    while ! eof(f)
        idx = 0
        line = readline(f)           
        line_list = split(line, " ")
        str_bfs = @time convert(String, bfs(convert(INT128, line_list[0]), line_list[1]))
        print("Line " * str(idx) + ": " * line_list[1] * ", " * str_bfs)
    end
end