import sys

def dec_to_bin(x):
    return str(bin(int(x))[2:])

def truth_table(bits, n):
    binary_n = dec_to_bin(n)
    binary_str = ''
    start_constant = (2**bits)-1
    length = (2**bits)
    if len(binary_n)!=length:
        zeroes_to_add = length-len(binary_n)
        final_binary_n = '0'*zeroes_to_add
        final_binary_n+=binary_n
        binary_str = final_binary_n
    else:
        binary_str = binary_n
    truth_table = []
    for c, num in zip(binary_str, reversed(range(start_constant + 1))):
        if len(dec_to_bin(num))!=bits:
            zeroes_to_add = bits-len(dec_to_bin(num))
            str_to_add = '0'*zeroes_to_add
            str_to_add+=dec_to_bin(num)
            temp = list(str_to_add)
            truth_table.append((tuple(temp), c))
        else:
            temp = list(dec_to_bin(num))
            truth_table.append((tuple(temp), c))
    return truth_table

def perceptron_training_algorithm(truth_table, bits):
    bias = 0
    weight = None
    if bits==2:
        weight = [0, 0]
    if bits==3:
        weight = [0, 0, 0]
    if bits==4:
        weight = [0, 0, 0, 0]
    epochs = []
    table = None
    for i in range(0, 100):
        table = []
        for row in truth_table:
            output = perceptron(step, weight, bias, row[0])
            if output!=row[-1]:
                #update weight
                f = float(row[-1]) - output
                second_vector_part = [float(ele)*f for ele in row[0]] 
                sum_list = []
                for (item1, item2) in  zip(weight, second_vector_part):
                    sum_list.append(item1+item2)
                weight = sum_list
                #Update bias
                bias = bias + f
                table.append((weight, bias))
            else:
                bias = output
                table.append((weight, bias))
        epochs.append((weight, bias))
        if len(epochs)>=2:
            if epochs[-1]==epochs[-2]:
                break    
    correct = 0
    for ele in table:
        if ele==(weight, bias):
            correct+=1
    return tuple(weight), bias, correct/len(truth_table)

def perceptron(A, w, b, x):
    sum = 0
    for f, o in zip(w, x):
        sum+=int(f)*int(o)
    return A(sum+float(b))

def step(num):
    if num>0:
        return 1
    else:
        return 0

bits = sys.argv[1]
n = sys.argv[2]
table = truth_table(int(bits), int(n))
output = perceptron_training_algorithm(table, int(bits))
print("Weight Vector: " + str(output[0]))
print("Bias Value: " + str(output[1]))
print("Accuracy: " + str(output[2]))
