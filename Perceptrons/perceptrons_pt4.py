import numpy as np
import sys
import ast
import math
import random

def check_point(point):
    t = point[0]**2+point[1]**2
    s = math.sqrt(t)
    if s<1:
        return True
    else:
        return False

def step(num):
    if num>0:
        return 1
    else:
        return 0

def sigmoid(num):
    return 1/(1+(math.e**(-num)))

def perceptron_network(A, x, weight_list, bias_list):
    new_f = np.vectorize(A)  # This creates a function that applies the original function to each element of a matrix individually
    a_0 = x
    a_l_prev = a_0
    for w, b in zip(weight_list[1:], bias_list[1:]):
        a_L = new_f(a_l_prev@w+b)
        a_l_prev = a_L
    return a_L

#XOR HAPPENS HERE
if len(sys.argv)==2:
    w1 = np.array([[2, -1], [2, -1]])
    w2 = np.array([[1], [1]])
    b1 = np.array([-1, 2])
    b2 = np.array([-1])
    weight_list = [None, w1, w2]
    bias_list = [None, b1, b2]
    x = ast.literal_eval(sys.argv[1])
    output_x_or = perceptron_network(step, x, weight_list, bias_list)
    print(output_x_or[0])

#Step-function diamond
if len(sys.argv)==3:
    weight_list = [None, np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]), np.array([[1], [1], [1], [1]])]
    bias_list = [None, np.array([1, 1, 1, 1]), np.array([-3])]
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    output_diamond = perceptron_network(step, (x, y), weight_list, bias_list)
    if output_diamond[0]==0:
        print('outside')
    else:
        print('inside')

#Circle challenge
else:
    weight_list = [None, np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]), np.array([[1], [1], [1], [1]])]
    bias_list = [None, np.array([1, 1, 1, 1]), np.array([-2.78])]
    points = []
    for i in range(0, 500):
        temp = []
        for x in range(0, 2):
            temp.append(random.uniform(-1, 1))
        points.append(tuple(temp))
    points_correct = 0
    points_incorrect = 0
    print("Incorrectly classified coordinates: ")
    for point in points:
        output_circle = perceptron_network(sigmoid, point, weight_list, bias_list)
        o = round(output_circle[0])            
        if (check_point(point)==False and o==0) or (check_point(point)==True and o==1):
            points_correct+=1
        else:
            points_incorrect+=1
            print(point)
    decimal_correct = (points_correct/500)
    percentage = "{:.0%}".format(decimal_correct)
    print("Classified correctly percentage: " + str(percentage))