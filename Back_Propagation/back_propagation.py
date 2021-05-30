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

def calc_error(expected_out, calculated_out):
    vec = np.array(expected_out-calculated_out)
    mag = np.linalg.norm(vec)
    return 0.5*(mag**2)

def step(num):
    if num>0:
        return 1
    else:
        return 0

def sigmoid(num):
    return 1/(1+(math.e**(-num)))

def sigmoid_derivative(dot_L, new_f):
    return new_f(dot_L)*(1-new_f(dot_L))

def back_propagation_sum_network(A, ADeriv, weight_list, bias_list, training, epochs, learning_rate):
    new_f = np.vectorize(A)  # This creates a function that applies the original function to each element of a matrix individually
    der_new_f = np.vectorize(ADeriv)
    for i in range(epochs):
        for tuple_values in training:
            x = np.array([tuple_values[0]])
            y = np.array([tuple_values[-1]])
            a_0 = x
            a_L = a_0
            #for each layer L in network
            a_list = [a_0]
            dot = [None]
            for w, b in zip(weight_list[1:], bias_list[1:]):
                dot_L = a_L@w+b
                a_L = new_f(dot_L)
                a_list.append(a_L)
                dot.append(dot_L)
            delta_N = (der_new_f(dot_L, new_f))*(y-a_L)
            delta = [None]
            for x in range(0, len(weight_list)-2):
                delta.append(None)
            delta.append(delta_N)
            #for each layer L in network (counting down from N-1)
            N = len(weight_list)-1
            for l in range(N-1, 0, -1):
                delta[l] = der_new_f(dot[l], new_f) * (delta[l+1] @ weight_list[l+1].T)
            #for each layer L in network:
            for i in range(1, N+1):
                bias_list[i] = bias_list[i]+(learning_rate*delta[i])
                weight_list[i] = weight_list[i]+((learning_rate*(a_list[i-1].T))@delta[i])
            print(a_list[-1])
            
def back_propagation_circle_network(A, ADeriv, weight_list, bias_list, training, epochs, learning_rate):
    new_f = np.vectorize(A)  # This creates a function that applies the original function to each element of a matrix individually
    der_new_f = np.vectorize(ADeriv)
    for z in range(0, epochs):
        list_of_final_training_values = []
        for tuple_values in training:
            x = np.array([tuple_values[0]])
            y = np.array([tuple_values[-1]])
            a_0 = x
            a_L = a_0
            #for each layer L in network
            a_list = [a_0]
            dot = [None]
            for w, b in zip(weight_list[1:], bias_list[1:]):
                dot_L = a_L@w+b
                a_L = new_f(dot_L)
                a_list.append(a_L)
                dot.append(dot_L)
            delta_N = (der_new_f(dot_L, new_f))*(y-a_L)
            delta = [None]
            for x in range(0, len(weight_list)-2):
                delta.append(None)
            delta.append(delta_N)
            #for each layer L in network (counting down from N-1)
            N = len(weight_list)-1
            for l in range(N-1, 0, -1):
                delta[l] = der_new_f(dot[l], new_f) * (delta[l+1] @ weight_list[l+1].T)
            #for each layer L in network:
            for i in range(1, N+1):
                bias_list[i] = bias_list[i]+(learning_rate*delta[i])
                weight_list[i] = weight_list[i]+((learning_rate*(a_list[i-1].T))@delta[i])
            list_of_final_training_values.append(a_list[-1][0][0])
        misclassified_points = 0
        for x in range(len(training)):
            if training[x][-1]!=round(list_of_final_training_values[x]):
                misclassified_points+=1
        print("Epoch number " + str(z) + ": " + str(misclassified_points) + " misclassified points")

if sys.argv[1]=="S":
    weight_list = [None, np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]]), np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]])]
    bias_list = [None, np.array([random.uniform(-1, 1), random.uniform(-1, 1)]), np.array([random.uniform(-1, 1)])] 
    training = [((0, 0), (0, 0)), ((0, 1), (0, 1)), ((1, 0), (0, 1)), ((1, 1), (1, 0))]
    back_propagation_sum_network(sigmoid, sigmoid_derivative, weight_list, bias_list, training, 5000, 1)
elif sys.argv[1]=="C":
    weight_list = [None, np.array([[random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]]), np.array([[random.uniform(-1, 1)], [random.uniform(-1, 1)], [random.uniform(-1, 1)], [random.uniform(-1, 1)]])]
    bias_list = [None, np.array([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]), np.array([random.uniform(-1, 1)])]
    points = []
    for i in range(0, 10000):
        temp = []
        for x in range(0, 2):
            temp.append(random.uniform(-1, 1))
        if (check_point(temp)==True):
            points.append((tuple(temp), (1)))
        else:
            points.append((tuple(temp), (0)))
    back_propagation_circle_network(sigmoid, sigmoid_derivative, weight_list, bias_list, points, 7500, 0.15)