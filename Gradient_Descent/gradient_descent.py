import sys
import numpy as np

threshold = 10**-8

def find_magnitude(vector):
    vec = np.array(vector)
    mag = np.linalg.norm(vec)
    return mag

def gradient_descent(function, pos_vector, gradient_vector):
    if pos_vector!= [0, 0] and find_magnitude(gradient_vector)<threshold:
        return
    lambda_val = 0.05
    vector = pos_vector
    negative_gradient_t = None
    function_A_or_B = None
    if function=="A":
        x = (8*vector[0])-(3*vector[1])+24
        y = 4*(vector[1]-5)-(3*vector[0])
        negative_gradient_t = [-x, -y]
        function_A_or_B = "A"
    else:
        x = 2*(vector[0]-(vector[1]**2))
        y = 2*(-2*vector[0]*vector[1]+(2*(vector[1]**3))+vector[1]-1)
        negative_gradient_t = [-x, -y]
        function_A_or_B = "B"
    negative_gradient_f = [element * lambda_val for element in negative_gradient_t]
    negative_gradient = tuple(negative_gradient_f)
    current_vector_position = []
    for f, o in zip(vector, negative_gradient):
        current_vector_position.append(f+o)
    print(f'Current location: {tuple(current_vector_position)} Current gradient vector: {negative_gradient}')
    #input()
    gradient_descent(function_A_or_B, current_vector_position, negative_gradient)


function = sys.argv[1]
start = [0, 0]
gradient_descent(function, start, None)