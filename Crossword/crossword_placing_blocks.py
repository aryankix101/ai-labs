import sys, random
from collections import deque

args_list = sys.argv
h_x_w = args_list[1]
num_rows = int(h_x_w[:h_x_w.index('x')])
num_cols = int(h_x_w[h_x_w.index('x')+1:])
num_blocks = int(args_list[2])
dict_txt = args_list[3]
start_words = []
board = []
for i in range(num_cols*num_rows):
    board.append('-')
if len(args_list)>4:
    for word in args_list[4:]:
        direc = word[0]
        r = int(word[1:word.index('x')])
        temp = []
        for n in word[word.index('x')+1:]:
            if n.isdigit():
                temp.append(n)
            else:
                break
        temp_str = ''.join(temp)
        c = int(temp_str)
        temp_2 = []
        for i in reversed(word):
            if i.isalpha() or i=="#":
                temp_2.append(i)
            else:
                break
        temp_2_str = ''.join(temp_2)
        add_word = temp_2_str[::-1].upper()
        start_words.append((direc, r, c, add_word))
#print(h_x_w, num_rows, num_cols, num_blocks, start_words)
for word in start_words:
    x_y = word[1]*num_cols + word[2] 
    if word[0] == 'V' or word[0] == 'v':
        for y in word[3]:
            board[x_y] = y
            x_y += num_cols
    if word[0] == 'H' or word[0] == 'h':
        for x in word[3]:
            board[x_y] = x
            x_y += 1

def print_puzzle(board,num_rows,num_cols):
    count = 0
    for i in range(num_rows):
        for x in range(num_cols):
            print(board[count] + "  ", end = "")
            count+=1
        print("")
print_puzzle(board,num_rows,num_cols)

def get_possible_values(board):
    possible_values = list()
    for idx, square in enumerate(board):
        if square=='-' and board[len(board)-(idx+1)]=='-':
            possible_values.append(idx)
    random.shuffle(possible_values)
    return possible_values

def area_fill(board, row, col):
    if row<0 or row>=num_rows or col<0 or col>=num_cols:
        return board
    x_y = (col + (row*num_cols))
    board[x_y] = '*'
    if col-1>=0 and board[x_y-1]!='*' and board[x_y-1]!="#":
        new_board = board.copy()
        board = area_fill(new_board, row, col-1)
    if row-1>=0 and board[x_y-num_cols]!='*' and board[x_y-num_cols]!="#":
        new_board = board.copy()
        board = area_fill(new_board, row-1, col)
    if row+1<num_rows and board[x_y+num_cols]!='*' and board[x_y+num_cols]!="#":
        new_board = board.copy()
        board = area_fill(new_board, row+1, col)
    if col+1<num_cols and board[x_y+1]!='*' and board[x_y+1]!="#":
        new_board = board.copy()
        board = area_fill(new_board, row, col+1)
    return board
    
def is_legal(board):
    #Everything should be connected (area fill?), each work should be 3 characters long minimum, 180 degrees symmetric board
    new_board = board.copy()
    if '-' in new_board:
        idx = new_board.index('-')
        area_filled = area_fill(new_board, idx//num_cols, idx%num_cols)
        isTrue = True
        if '-' not in area_filled:
            isTrue = True
        else:
            return False
    temp_board = new_board.copy()
    for i in range(len(temp_board)):
        if temp_board[i] != '-' and temp_board[i] != '#':
            temp_board[i] = '-'
    if temp_board==temp_board[::-1]:
        isTrue = True
    else:
        return False
    return isTrue

def place_symmetrical_blocks(board):
    sym_blocks = set()
    blocks = []
    for i in range(len(board)):
        if board[i]=="#":
            blocks.append(i)
    for b in blocks:
        symmetrical_index = len(board) - (b+1)
        if board[symmetrical_index]=='-':
            sym_blocks.add(symmetrical_index)
    for s in sym_blocks:
        board[s] = "#"
    return board

def find_implied_fillers(board, idx):
    implied_blocks = set()
    
    has_iterated_1 = False
    temp_right = idx
    if ((temp_right+1)%num_cols)!=0:
        count_r = 0
        temp_right = idx+1
        if ((temp_right+1)%num_cols)!=0:
            while board[temp_right]=='-' and count_r<2 and ((temp_right+1)%num_cols)!=0:
                temp_right+=1
                count_r+=1
                has_iterated_1 = True
            if (temp_right)<=len(board)-1 and (temp_right)>=0:
                if (board[temp_right]=="#" or (board[temp_right]=="-" and ((temp_right+1)%num_cols)==0)) and has_iterated_1:
                    if count_r==1 and board[temp_right]=="#":
                        implied_blocks.add(temp_right-1)
                    if (board[temp_right]=="-" and ((temp_right+1)%num_cols)==0) and count_r==1:
                        implied_blocks.add(temp_right)
                        implied_blocks.add(temp_right-1)
                    if count_r==2 and board[temp_right]=="#":
                        implied_blocks.add(temp_right-1)
                        implied_blocks.add(temp_right-2)
        elif ((temp_right+1)%num_cols)==0:
            if board[temp_right]=="-":
                implied_blocks.add(temp_right)

    has_iterated_2 = False
    temp_left = idx
    if ((temp_left)%num_cols)!=0:
        count_l = 0
        temp_left = idx-1
        if ((temp_left)%num_cols)!=0:
            while board[temp_left]=='-' and count_l<2 and ((temp_left)%num_cols)!=0:
                temp_left-=1
                count_l+=1
                has_iterated_2 = True
            if (temp_left)<=len(board)-1 and (temp_left)>=0:
                if (board[temp_left]=="#" or (board[temp_left]=="-" and ((temp_left)%num_cols)==0)) and has_iterated_2:
                    if count_l==1 and board[temp_left]=="#":
                        implied_blocks.add(temp_left+1)
                    if (board[temp_left]=="-" and ((temp_left)%num_cols)==0) and count_l==1:
                        implied_blocks.add(temp_left)
                        implied_blocks.add(temp_left+1)
                    if count_l==2 and board[temp_left]=="#":
                        implied_blocks.add(temp_left+1)
                        implied_blocks.add(temp_left+2)
        elif ((temp_left)%num_cols)==0:
            if board[temp_left]=="-":
                implied_blocks.add(temp_left)


    has_iterated_3 = False
    temp_up = idx
    if temp_up>=num_cols:
        count_up = 0
        temp_up = idx-num_cols
        if temp_up>=num_cols:
            while board[temp_up]=="-" and temp_up>=num_cols and count_up<2:
                temp_up-=num_cols
                count_up+=1
                has_iterated_3 = True
            if (temp_up)<=len(board)-1 and (temp_up)>=0:
                if (board[temp_up]=="#" or (board[temp_up]=="-" and temp_up<=num_cols)) and has_iterated_3:
                    if count_up==1 and board[temp_up]=="#":
                            implied_blocks.add(temp_up+num_cols)
                    if (board[temp_up]=="-" and temp_up<=num_cols) and count_up==1:
                        implied_blocks.add(temp_up)
                        implied_blocks.add(temp_up+num_cols)
                    if count_up==2 and board[temp_up]=="#":
                        implied_blocks.add(temp_up+num_cols)
                        implied_blocks.add(temp_up+(2*num_cols))
        elif temp_up<=num_cols:
            if board[temp_up]=="-":
                implied_blocks.add(temp_up)

    has_iterated_4 = False
    temp_down = idx
    if temp_down<=((num_rows-1)*num_cols)-1:
        count_down = 0
        temp_down = idx+num_cols
        if temp_down<=((num_rows-1)*num_cols)-1:
            while board[temp_down]=="-" and temp_down<=((num_rows-1)*num_cols)-1 and count_down<2:
                temp_down+=num_cols
                count_down+=1
                has_iterated_4 = True
            if (temp_down)<=len(board)-1 and (temp_down)>=0:
                if (board[temp_down]=="#" or (board[temp_down]=="-" and temp_down>=((num_rows-1)*num_cols)-1)) and has_iterated_4:
                    if count_down==1 and board[temp_down]=="#":
                            implied_blocks.add(temp_down-num_cols)
                    if (board[temp_down]=="-" and temp_down>=((num_rows-1)*num_cols)-1) and count_down==2:
                        implied_blocks.add(temp_down)
                        implied_blocks.add(temp_down-num_cols)
                    if count_down==2 and board[temp_down]=="#":
                        implied_blocks.add(temp_down-num_cols)
                        implied_blocks.add(temp_down-(2*num_cols))
        elif temp_down>=((num_rows-1)*num_cols)-1:
            if board[temp_down]=="-":
                implied_blocks.add(temp_down)
    return implied_blocks

def find_implied(board):
    #take half of all the blocks and have them find if they are allowing 2/1 length words, find implied blocks of them (aka filling it in), then at the end, find the symmetrical of all the implied blocks. Return that.
    blocks_to_look_t = []
    for i in range(len(board)):
        if board[i]=="#" and board[len(board) - (i+1)]=="#":
            blocks_to_look_t.append(i)
    blocks_to_look = blocks_to_look_t[:len(blocks_to_look_t)//2]
    implied_blocks = []
    for c in blocks_to_look:
        implied_blocks.append(find_implied_fillers(board, c))
    implied_blocks_set = set()
    for x in implied_blocks:
        for y in x:
            symmetrical_index = len(board) - (y+1)
            if board[y]=='-' and board[symmetrical_index]=="-":
                implied_blocks_set.add(symmetrical_index)
                implied_blocks_set.add(y)
    return implied_blocks_set

def length_3_words_only(board,index):
    left = False
    isBlock = True
    index_left = index
    while (index_left%num_cols)>0:
        index_left-=1
        if (index_left%num_cols)==0 and board[index_left]=='#':
            left = True
        if board[index_left]!='#':
            isBlock = False
            break
    count = 0
    if not isBlock:
        while (index_left%num_cols)>0:
            index_left-=1
            if board[index_left]=='#':
                break
            else:
                count+=1
    if index%num_cols==0 or count>=2:
        left = True
    #else:
        #return False

    right = False
    isBlock = True
    index_right = index
    while ((index_right+1)%num_cols)!=0:
        index_right+=1
        if ((index_right+1)%num_cols)==0 and board[index_right]=='#':
            right = True
        if board[index_right]!='#':
            isBlock = False
            break
    count = 0
    if not isBlock:
        while ((index_right+1)%num_cols)!=0:
            index_right+=1
            if board[index_right]=='#':
                break
            else:
                count+=1
    if index%num_cols==num_cols-1 or count>=2:
        right = True
    #else:
        #return False

    up = False
    isBlock = True
    index_up = index
    while index_up>=num_cols:
        index_up-=num_cols
        if index_up<num_cols and board[index_up]=='#':
            up = True
        if board[index_up]!='#':
            isBlock = False
            break
    count = 0
    if not isBlock:
        while index_up>=num_cols:
            index_up-=num_cols
            if board[index_up]=='#':
                break
            else:
                count+=1
    if count>=2 or index<num_cols:
        up = True
    #else:
        #return False

    down = False
    isBlock = True
    index_down = index
    while index_down<=((num_rows-1)*num_cols)-1:
        index_down+=num_cols
        if index_down>((num_rows-1)*num_cols)-1 and board[index_down]=='#':
            down = True
        if board[index_down]!='#':
            isBlock = False
            break
    count = 0
    if not isBlock:
        while index_down<=((num_rows-1)*num_cols)-1:
            index_down+=num_cols
            if board[index_down]=='#':
                break
            else:
                count+=1
    if index>=len(board)-num_cols or count>=2:
        down = True
    #else:
        #return False
    
    if left and right and up and down:
        return True
    else:
        return False

def board_checker_length_3(board):
    blocks_to_look_t = []
    for index, block in enumerate(board):
        if block == "#":
            blocks_to_look_t.append(index)
    blocks_to_look = blocks_to_look_t[:len(blocks_to_look_t)//2]
    for i in blocks_to_look:
        if not length_3_words_only(board, i):
            return False
    return True

def bfs(board):
    q = deque(find_implied(board))
    visited = set(q)
    if len(q)==0 and board_checker_length_3(board):
        return board
    while q:
        v = q.popleft()
        if board.count("#")>=num_blocks:   
            return None
        board[v] = "#"
        for u in find_implied(board):
            if u not in visited:
                q.append(u)
                visited.add(u)
    if board_checker_length_3(board)==False:
        return None
    return board

def backtracking(board, ongoing_blocks, end_blocks):
    if ongoing_blocks==end_blocks and is_legal(board):
        return board
    elif not is_legal(board):
        return None
    elif ongoing_blocks>=end_blocks:
        return None
    for val in get_possible_values(board):
        new_board = board.copy()
        new_board[val] = "#"
        new_board[len(board)-(val+1)] = "#"
        updated_board = bfs(new_board)
        if updated_board is not None:
            result = backtracking(updated_board, updated_board.count("#"), end_blocks)
        else:
            result = None
        if result is not None:
            return result
    return None

print("")
new_board = place_symmetrical_blocks(board)
final_blocking_board = backtracking(new_board, new_board.count("#"), num_blocks)
print_puzzle(final_blocking_board, num_rows, num_cols)