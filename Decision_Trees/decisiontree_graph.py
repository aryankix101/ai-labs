import pygraphviz as pgv
import sys
import time
import math

with open(sys.argv[1]) as f:
    line_list = [line.strip().split(',') for line in f]

table = zip(*line_list)
dataset = []
for t in table:
    dataset.append(list(t))

class Node:
    def __init__(self, name, depth, is_feature, is_leaf, children, is_start, outcome):
        self.name = name
        self.depth = depth
        self.is_feature = is_feature
        self.is_leaf = is_leaf
        self.children = children
        self.is_start = is_start
        self.outcome = outcome

def choose_feature(features, information_gain):
    idx = information_gain.index(max(information_gain))
    return features[idx]

def reduce_data_set(feature, dataset):
    #print(feature, dataset)
    feature_t = feature.copy()
    feature_t.pop(0)
    possible_values = set(feature_t)
    new_datasets = []
    for val in possible_values:
        temp_indexes = []
        for i in range(len(feature)):
            if feature[i]==val or i==0:  
                temp_indexes.append(i)
        new_dataset = []
        for list_feature in dataset:
            temp_list = []
            for index in temp_indexes:
                temp_list.append(list_feature[index])
            new_dataset.append(temp_list)
        new_datasets.append(new_dataset)
    values = list(possible_values)
    return new_datasets, values

def find_entropy(feature):
    feature_t = feature.copy()
    #feature_t.pop(0)
    possible_values = set(feature_t)
    length = len(feature_t)
    log_values = []
    for val in possible_values:
        log_values.append((feature_t.count(val)/length)*math.log(feature_t.count(val)/length, 2))
    return -1*sum(log_values)

def find_starting_entropy(feature):
    feature_t = feature.copy()
    feature_t.pop(0)
    possible_values = set(feature_t)
    length = len(feature_t)
    log_values = []
    for val in possible_values:
        log_values.append((feature_t.count(val)/length)*math.log(feature_t.count(val)/length, 2))
    return -1*sum(log_values)

def information_gain(feature, dataset, orig_entropy):
    feature_t = feature.copy()
    name = feature_t.pop(0)
    possible_values = set(feature_t)
    length = len(feature_t)
    entropy_of_particular_data_set = []
    log_values = []
    for val in possible_values:
        temp_indexes = []
        for i in range(len(feature)):
            if feature[i]==val:  
                temp_indexes.append(i)
        entropy_find = []
        look = dataset[-1]
        for idx in temp_indexes:
            entropy_find.append(look[idx])
        entropy = find_entropy(entropy_find)
        log_values.append((feature_t.count(val)/length)*entropy)
    return orig_entropy-sum(log_values)

def print_tree(nodes):
    for node in nodes:
        if node.is_feature:
            print(node.depth*' ' + '* ' + node.name + '?')
        elif node.is_leaf:
            print(node.depth*' ' + '* ' + node.name + ' --> ' + node.outcome)
        else:
            print(node.depth*' ' + '* ' + node.name)

def generate_decision_tree(dataset, depth, nodes):
    start_entropy = find_starting_entropy(dataset[-1])
    gains = []
    for feature in dataset[0:-1]:
        gains.append(information_gain(feature, dataset, start_entropy))
    highest_info_gain_feature = choose_feature(dataset, gains)
    name = highest_info_gain_feature.pop(0)
    values = set(highest_info_gain_feature)
    if depth==-1:
        head = Node(name, depth+1, True, False, list(values), True, None)
        nodes.append(head)
    else:
        feature_node = Node(name, depth+1, True, False, list(values), False, None)
        node_parent = nodes[-1]
        node_parent.children.append(name)
        nodes.append(feature_node)
    highest_info_gain_feature.insert(0, name)
    new_data_sets, possible_values = reduce_data_set(highest_info_gain_feature, dataset)
    depth+=1
    for idx, data_set in enumerate(new_data_sets):
        if find_starting_entropy(data_set[-1])==0:
            node = Node(possible_values[idx], depth+1, False, True, [], False, data_set[-1][1])
            nodes.append(node)
        else:
            node = Node(possible_values[idx], depth+1, False, False, [], False, None)
            nodes.append(node)
            generate_decision_tree(data_set, depth+1, nodes)
    return nodes


#head = (generate_decision_tree(dataset, -1, None))
#dfs_binary_tree(head)
nodes = generate_decision_tree(dataset, -1, [])
#for node in nodes:
    #print(node.depth, node.name, node.children)
print_tree(nodes)
