import ast
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

def check(n, w, b):
    table = truth_table(len(w), n)
    correct = 0
    for input in table:
        output = perceptron(step, w, b, input[0])
        if output==int(input[-1]):
            correct+=1
    return correct/len(table)

n = sys.argv[1]
t = ast.literal_eval(sys.argv[2])
b = sys.argv[3]
print(check(n, t, b))