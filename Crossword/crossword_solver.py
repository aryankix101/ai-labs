import sys, random
from collections import deque
import time

args_list = sys.argv
h_x_w = args_list[1]
num_rows = int(h_x_w[:h_x_w.index('x')])
num_cols = int(h_x_w[h_x_w.index('x')+1:])
num_blocks = int(args_list[2])
dict_txt = args_list[3]
start_words = []
board = []
case = ""
tester = ""
for idx in range(len(board)):
    if board[idx].isalpha():
        temp = board[idx]
        t2 = temp.upper()
        board[idx] = t2
        tester=t2
if tester.islower():
    case = "l"
if tester.isupper():
    case = "u"
if tester=="":
    case = "u"
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
    if (num_rows and num_cols)<=4:
        return implied_blocks
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
    #print(implied_blocks)
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

#Start of placing words setup + algo
with open(dict_txt) as f: 
    temp_set_of_words = set()
    temp_set_of_lengths = set()
    for idx, line in enumerate(f):
            word = line.rstrip()
            if word.isalpha() and len(word)>=3:
                #and (len(word)<=num_rows or len(word)<=num_cols)
                temp_set_of_words.add(word)
                temp_set_of_lengths.add(len(word))
sorted(temp_set_of_words)
dict_of_words = {}
for l in temp_set_of_lengths:
    temp_set = set()
    for w in temp_set_of_words:
        if len(w)==l:
            temp_set.add(w)
    dict_of_words.update({l:temp_set})

def place_word(board, word, start_index, end_index, dir):
    temp_str = word.upper()
    if dir=="V":
        temp = start_index
        while temp<=end_index:
            if board[temp]=="-":
                board[temp] = temp_str[0].upper()
                temp_str = temp_str[1:]
            elif board[temp].isalpha():
                temp_str = temp_str[1:]
            temp+=num_cols
    if dir=="H":
        temp = start_index
        while temp<=end_index:
            if board[temp]=="-":
                board[temp] = temp_str[0].upper()
                temp_str = temp_str[1:]
            elif board[temp].isalpha():
                temp_str = temp_str[1:]
            temp+=1
    return board

def get_next_var(board, dict_of_sets):
    min_list = []
    min_dict = []
    for key, value in dict_of_sets.items():
        if "V" in key:
            look_v = []
            t = key[0]
            while t<=key[1]:
                look_v.append(board[t])
                t+=num_cols
            if "-" in look_v:
                min_list.append(len(value))
                min_dict.append(key)
        if "H" in key:
            look_h = []
            t = key[0]
            while t<=key[1]:
                look_h.append(board[t])
                t+=1
            if "-" in look_h:
                min_list.append(len(value))
                min_dict.append(key)
    min_val = min(min_list)
    min_idx = min_list.index(min_val)
    min_word_place = min_dict[min_idx]
    return min_word_place

def word_placements(board):
    list_of_blocks = []
    for idx in range(len(board)):
        if board[idx]=="#":
            list_of_blocks.append(idx)
    possible_words = []
    for block in list_of_blocks:
        #Down
        if block<=((num_rows-3)*num_cols)-1:
            temp_down = block+num_cols
            down_characters = []
            indices = []
            down_length = 0
            if board[temp_down]!="#":
                down_characters.append(board[temp_down])
                down_length+=1
                indices.append(temp_down)
                while board[temp_down]!="#":
                    temp_down+=num_cols
                    if board[temp_down]=="#":
                        break
                    down_characters.append(board[temp_down])
                    down_length+=1
                    indices.append(temp_down)
                    if temp_down>((num_rows-1)*num_cols)-1:
                        break
                if "-" in down_characters:
                    possible_words.append([indices[0], indices[-1], "V", len(down_characters), down_characters])
        #Up
        if block>=(num_cols*3):
            temp_up = block-num_cols
            up_characters = []
            indices = []
            up_length = 0
            if board[temp_up]!="#":
                up_characters.append(board[temp_up])
                up_length+=1
                indices.append(temp_up)
                while board[temp_up]!="#":
                    temp_up-=num_cols
                    if board[temp_up]=="#":
                        break
                    up_characters.append(board[temp_up])
                    up_length+=1
                    indices.append(temp_up)
                    if temp_up<num_cols:
                        break
                if "-" in up_characters:
                    up_characters.reverse()
                    possible_words.append([indices[-1], indices[0], "V", len(up_characters), up_characters])
        #Right
        if ((block+1)%num_cols)!=0:
            temp_right = block+1
            right_characters = []
            indices = []
            right_length = 0
            if board[temp_right]!="#":
                right_characters.append(board[temp_right])
                right_length+=1
                indices.append(temp_right)
                while board[temp_right]!="#":
                    temp_right+=1
                    if board[temp_right]=="#":
                        break
                    right_characters.append(board[temp_right])
                    right_length+=1
                    indices.append(temp_right)
                    if ((temp_right+1)%num_cols)==0:
                        break
                if "-" in right_characters:
                    possible_words.append([indices[0], indices[-1], "H", len(right_characters), right_characters])
        #Left
        if block%num_cols!=0:
            temp_left = block-1
            left_characters = []
            indices = []
            left_length = 0
            if board[temp_left]!="#":
                left_characters.append(board[temp_left])
                left_length+=1
                indices.append(temp_left)
                while board[temp_left]!="#":
                    temp_left-=1
                    if board[temp_left]=="#":
                        break
                    left_characters.append(board[temp_left])
                    left_length+=1
                    indices.append(temp_left)
                    if temp_left%num_cols==0:
                        break
                if "-" in left_characters:
                    left_characters.reverse()
                    possible_words.append([indices[-1], indices[0], "H", len(left_characters), left_characters])
    spaces_to_look_from_vertical = []
    spaces_to_look_from_horizontal = []
    for x in range(len(board)):
        if x<num_cols:
            spaces_to_look_from_vertical.append(x)
        if x%num_cols==0:
            spaces_to_look_from_horizontal.append(x)
    for v in spaces_to_look_from_vertical:
        temp_down=v
        possible_word = []
        if board[temp_down]!="#":
            possible_word.append(board[temp_down])
            while temp_down<=((num_rows-1)*num_cols)-1:
                temp_down+=num_cols
                possible_word.append(board[temp_down])
            if "#" not in possible_word and "-" in possible_word:
                possible_words.append([v, temp_down, "V", num_rows, possible_word])
    for h in spaces_to_look_from_horizontal:
        temp_right=h
        possible_word = []
        if board[temp_right]!="#":
            possible_word.append(board[temp_right])
            while ((temp_right+1)%num_cols)!=0:
                temp_right+=1
                possible_word.append(board[temp_right])
            if "#" not in possible_word and "-" in possible_word:
                possible_words.append([h, temp_right, "H", num_cols, possible_word])
    return possible_words

def check_words(board):
    list_of_blocks = []
    for idx in range(len(board)):
        if board[idx]=="#":
            list_of_blocks.append(idx)
    possible_words = []
    for block in list_of_blocks:
        #Down
        if block<=((num_rows-3)*num_cols)-1:
            temp_down = block+num_cols
            down_characters = []
            indices = []
            down_length = 0
            if board[temp_down]!="#":
                down_characters.append(board[temp_down])
                down_length+=1
                indices.append(temp_down)
                while board[temp_down]!="#":
                    temp_down+=num_cols
                    if board[temp_down]=="#":
                        break
                    down_characters.append(board[temp_down])
                    down_length+=1
                    indices.append(temp_down)
                    if temp_down>((num_rows-1)*num_cols)-1:
                        break
                possible_words.append([indices[0], indices[-1], "V", len(down_characters), down_characters])
        #Up
        if block>=(num_cols*3):
            temp_up = block-num_cols
            up_characters = []
            indices = []
            up_length = 0
            if board[temp_up]!="#":
                up_characters.append(board[temp_up])
                up_length+=1
                indices.append(temp_up)
                while board[temp_up]!="#":
                    temp_up-=num_cols
                    if board[temp_up]=="#":
                        break
                    up_characters.append(board[temp_up])
                    up_length+=1
                    indices.append(temp_up)
                    if temp_up<num_cols:
                        break
                up_characters.reverse()
                possible_words.append([indices[-1], indices[0], "V", len(up_characters), up_characters])
        #Right
        if ((block+1)%num_cols)!=0:
            temp_right = block+1
            right_characters = []
            indices = []
            right_length = 0
            if board[temp_right]!="#":
                right_characters.append(board[temp_right])
                right_length+=1
                indices.append(temp_right)
                while board[temp_right]!="#":
                    temp_right+=1
                    if board[temp_right]=="#":
                        break
                    right_characters.append(board[temp_right])
                    right_length+=1
                    indices.append(temp_right)
                    if ((temp_right+1)%num_cols)==0:
                        break
                possible_words.append([indices[0], indices[-1], "H", len(right_characters), right_characters])
        #Left
        if block%num_cols!=0:
            temp_left = block-1
            left_characters = []
            indices = []
            left_length = 0
            if board[temp_left]!="#":
                left_characters.append(board[temp_left])
                left_length+=1
                indices.append(temp_left)
                while board[temp_left]!="#":
                    temp_left-=1
                    if board[temp_left]=="#":
                        break
                    left_characters.append(board[temp_left])
                    left_length+=1
                    indices.append(temp_left)
                    if temp_left%num_cols==0:
                        break
                left_characters.reverse()
                possible_words.append([indices[-1], indices[0], "H", len(left_characters), left_characters])
    spaces_to_look_from_vertical = []
    spaces_to_look_from_horizontal = []
    for x in range(len(board)):
        if x<num_cols:
            spaces_to_look_from_vertical.append(x)
        if x%num_cols==0:
            spaces_to_look_from_horizontal.append(x)
    for v in spaces_to_look_from_vertical:
        temp_down=v
        possible_word = []
        if board[temp_down]!="#":
            possible_word.append(board[temp_down])
            while temp_down<=((num_rows-1)*num_cols)-1:
                temp_down+=num_cols
                possible_word.append(board[temp_down])
            if "#" not in possible_word:
                possible_words.append([v, temp_down, "V", num_rows, possible_word])
    for h in spaces_to_look_from_horizontal:
        temp_right=h
        possible_word = []
        if board[temp_right]!="#":
            possible_word.append(board[temp_right])
            while ((temp_right+1)%num_cols)!=0:
                temp_right+=1
                possible_word.append(board[temp_right])
            if "#" not in possible_word:
                possible_words.append([h, temp_right, "H", num_cols, possible_word])
    return possible_words

def generate_sets(board):
    dict_of_placements = {}
    possible_placements = word_placements(board)
    for word_placement in possible_placements:
        potential_words = set()
        str1 = ""
        str1 = str1.join(word_placement[-1])
        length = word_placement[3]
        bol = True
        for c in str1:
            if c!="-":
                bol = False
                break
        if bol:
            words = dict_of_words.get(length)
            for w in words:
                potential_words.add(w)
        else:
            count = 0
            if dict_of_words.get(length)!=None:
                for w in dict_of_words.get(length):
                    isTrue = True
                    for x, y in zip(str1, w):
                        if x=="-":
                            continue
                        else:
                            if x.upper()!=y.upper():
                                isTrue = False
                                break
                    if isTrue:
                        potential_words.add(w)
        dict_of_placements.update({(word_placement[0], word_placement[1], word_placement[2]):potential_words})
    return dict_of_placements

def remove_words(updated_board, dictionary, move, val):
    key_of_move = val
    del dictionary[val]
    if "H" in key_of_move:
        for key, value in dictionary.items():
            if move in value:
                value.remove(move)
        look = []
        temp = key_of_move[0]
        while temp<=key_of_move[1]:
            look.append(temp)
            temp+=1
        for key, value in dictionary.items():
            if "V" in key:
                look_v = []
                t = key[0]
                while t<=key[1]:
                    look_v.append(t)
                    t+=num_cols
                a_set = set(look)
                b_set = set(look_v)
                word = []
                if (a_set & b_set):
                    for v_idx in look_v:
                        word.append(updated_board[v_idx])
                    str1 = ""
                    str1 = str1.join(word)
                    temp_l = set()
                    for w in dictionary.get(key):
                        for x, y in zip(str1, w):
                            if x=="-":
                                continue
                            else:
                                if x.upper()!=y.upper():
                                    temp_l.add(w)
                    for word_to_remove in temp_l:
                        dictionary.get(key).remove(word_to_remove)
                else:
                    continue    
    if "V" in key_of_move:    
        for key, value in dictionary.items():
            if move in value:
                value.remove(move)
        look = []
        temp = key_of_move[0]
        while temp<=key_of_move[1]:
            look.append(temp)
            temp+=1
        for key, value in dictionary.items():
            if "H" in key:
                look_h = []
                t = key[0]
                while t<=key[1]:
                    look_h.append(t)
                    t+=1
                a_set = set(look)
                b_set = set(look_h)
                word = []
                if (a_set & b_set):
                    for h_idx in look_h:
                        word.append(updated_board[h_idx])
                    str1 = ""
                    str1 = str1.join(word)
                    temp_l = set()
                    for w in dictionary.get(key):
                        for x, y in zip(str1, w):
                            if x=="-":
                                continue
                            else:
                                if x.upper()!=y.upper():
                                    temp_l.add(w)
                    for word_to_remove in temp_l:
                        dictionary.get(key).remove(word_to_remove)
                else:
                    continue  
    return dictionary

def get_possible_moves(board, val, dict_of_sets):
    possible_moves = set()
    possible_moves = dict_of_sets.get(val)
    return possible_moves

def goal_test(b):
    if '-' in b:
        return False
    return True

def check_validity(b):
    if "-" not in b:
        possible_placements = check_words(b)
        for word_placement in possible_placements:
            str1 = ""
            str1 = str1.join(word_placement[-1])
            length = word_placement[3]
            set_length = dict_of_words.get(length)
            if str1.lower() not in set_length:
                return False
    return True

def backtracking(board, d):
    #print("")
    #print_puzzle(board, num_rows, num_cols)
    if goal_test(board):
        #print(d)
        return board
    val = get_next_var(board, d)
    #print(val)
    for move in get_possible_moves(board, val, d):
        #print(move)
        #input()
        new_board = board.copy()
        updated_board = place_word(new_board, move, val[0], val[1], val[2])
        #FIND A WAY TO GET RID OF/SPEED UP CHECK VALIDITY
        if check_validity(updated_board): 
            sets_dict = {x: d[x].copy() for x in d}
            sets_dict = remove_words(updated_board, sets_dict, move, val)
            result = backtracking(updated_board, sets_dict)
        else:
            result = None
        if result is not None:
            return result
    return None

dict_of_sets = generate_sets(final_blocking_board)
fboard = backtracking(final_blocking_board, dict_of_sets)
print("")
print_puzzle(fboard, num_rows, num_cols)