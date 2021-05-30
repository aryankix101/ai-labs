import sys
import ast

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

#XOR HAPPENS HERE
def perceptron_network(input_val):
    o3 = perceptron(step, (2, 2), -1, input_val)
    o4 = perceptron(step, (-1, -1), 2, input_val)
    o5 = perceptron(step, (1, 1), -1, (o3, o4))
    return o5

x = ast.literal_eval(sys.argv[1])
output = perceptron_network(x)
print(output)