import time
import random

length_of_state = 35
start_state = []
for i in range(length_of_state):
    start_state.append(None)

length_of_state_2 = 40
start_state_2 = []
for i in range(length_of_state_2):
    start_state_2.append(None)

def test_solution(state):
    length = len(state)
    for var in range(length):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                #return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                #return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                #return False
    return True

def get_next_unassigned_var(state):
    return state.index(None)

def get_sorted_values(state, var):
    list_of_values = []
    for i in range(len(state)):
        isTrue = True
        if i in state[0:var]:
            isTrue = False
        temp_r1 = var
        temp_c1 = i
        while(temp_c1 < len(state) and temp_r1 >= 0):
            temp_r1 -= 1
            temp_c1 += 1
            if state[temp_r1] == temp_c1:
                isTrue = False
        temp_r2 = var
        temp_c2 = i
        while(temp_c2 >= 0 and temp_r2 >= 0):
            temp_c2 -= 1
            temp_r2 -= 1
            if state[temp_r2] == temp_c2:
                isTrue = False
        if isTrue:
            list_of_values.append(i)
    
    return random.sample(list_of_values, len(list_of_values))


def goal_test(state):
    if None not in state:
        return True
    return False

def csp_backtracking(state):
    if goal_test(state): 
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        new_state = state.copy()
        new_state[var] = val
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

def generate_min_conflict(state, var):
    conflicts_list = []
    for i in range(len(state)):
        conflicts = 0
        temp_r = var
        temp_c = i
        while(temp_r>0):
            temp_r -= 1
            if state[temp_r]==temp_c:
                conflicts+=1
        temp_r_back = var
        temp_c_back = i
        while(temp_r_back < len(state)-1):
            temp_r_back += 1
            if state[temp_r_back]==temp_c_back:
                conflicts+=1
        temp_r1 = var
        temp_c1 = i
        while(temp_r1 > 0 and temp_c1 < len(state)):
            temp_r1 -= 1
            temp_c1 += 1
            if state[temp_r1] == temp_c1:
                conflicts+=1
        temp_r2 = var
        temp_c2 = i
        while(temp_r2 > 0 and temp_c2 > 0):
            temp_c2 -= 1
            temp_r2 -= 1
            if state[temp_r2] == temp_c2:
                conflicts+=1
        temp_r3 = var
        temp_c3 = i
        while(temp_r3 < len(state)-1 and temp_c3 < len(state)-1):
            temp_r3 += 1
            temp_c3 += 1
            if state[temp_r3] == temp_c3:
                conflicts+=1
        temp_r4 = var
        temp_c4 = i
        while(temp_r4 < len(state)-1 and temp_c4 >= 0):
            temp_c4 -= 1
            temp_r4 += 1
            if state[temp_r4] == temp_c4:
                conflicts+=1
        conflicts_list.append(conflicts)
    min_value = min(conflicts_list)
    min_list = [i for i, x in enumerate(conflicts_list) if x==min_value]
    idx_min = random.choice(min_list)
    return [idx_min, min_value]

def find_number_of_conflicts(state, var, val):
    conflicts = 0
    temp = var
    temp_ca = val
    while(temp>0):
        temp -= 1
        if state[temp]==temp_ca:
            conflicts+=1
    temp_r = var
    temp_c = val
    while(temp_r < len(state)-1):
        temp_r += 1
        if state[temp_r]==temp_c:
            conflicts+=1
    temp_r1 = var
    temp_c1 = val
    while(temp_r1 < len(state)-1 and temp_c1 < len(state)-1):
        temp_r1 += 1
        temp_c1 += 1
        if state[temp_r1] == temp_c1:
            conflicts+=1
    temp_r2 = var
    temp_c2 = val
    while(temp_r2 < len(state)-1 and temp_c2 > 0):
        temp_c2 -= 1
        temp_r2 += 1
        if state[temp_r2] == temp_c2:
            conflicts+=1
    temp_r3 = var
    temp_c3 = val
    while(temp_r3 > 0 and temp_c3 < len(state)):
        temp_r3 -= 1
        temp_c3 += 1
        if state[temp_r3] == temp_c3:
            conflicts+=1
    temp_r4 = var
    temp_c4 = val
    while(temp_r4 > 0 and temp_c4 > 0):
        temp_c4 -= 1
        temp_r4 -= 1
        if state[temp_r4] == temp_c4:
            conflicts+=1
    return conflicts

def incremental_repair(state):
    list_of_conflicts = []
    for idx, col in enumerate(state):
        new_val = generate_min_conflict(state, idx)
        state[idx] = new_val[0]
    for idx, col in enumerate(state):
        conflicts = find_number_of_conflicts(state, idx, col)
        list_of_conflicts.append(conflicts)
    #print(list_of_conflicts)
    while sum(list_of_conflicts)!=0:
        max_value = max(list_of_conflicts)
        max_list = [i for i, x in enumerate(list_of_conflicts) if x==max_value]
        idx_max = random.choice(((max_list)))
        #print(max_value, idx_max)
        new_val = generate_min_conflict(state, idx_max)
        #print(new_val)
        state[idx_max] = new_val[0]
        list_of_conflicts[idx_max] = new_val[1]
        temp_list = list_of_conflicts.copy()
        temp = sum(temp_list)
        for idx, col in enumerate(state):
            if idx!=idx_max:
                new_val = find_number_of_conflicts(state, idx, col)
                list_of_conflicts[idx] = new_val
        #print(list_of_conflicts)
        if sum(list_of_conflicts)>temp:
            list_of_conflicts = temp_list
        else:
            print("Number of conflicts: " + str(sum(list_of_conflicts)), state)  
    return state
 
total_start = time.perf_counter()
state = csp_backtracking(start_state)
print(state)
print(test_solution(state))

state_2 = csp_backtracking(start_state_2)
print(state_2)
print(test_solution(state))

incremental_repair_state = incremental_repair(start_state)
print(test_solution(incremental_repair_state))

incremental_repair_state_2 = incremental_repair(start_state_2)
print(test_solution(incremental_repair_state_2))

total_end = time.perf_counter()
print(str(total_end-total_start) + " seconds")