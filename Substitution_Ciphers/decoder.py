from math import log
import random
import sys
import time
from collections import Counter

POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8

d = {}
with open("ngrams.txt") as f:
    #line_list = [line.strip() for line in f]
    for line in f:
        t = line.strip()
        word_freq = t.split()
        d.update({word_freq[0]:int(word_freq[1])})

encode_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#cipher_alphabet = 'XRPHIWGSONFQDZEYVJKMATUCLB'

def decoded_message(encoded_textblock, candidate_cipher_alphabet):
    decoded_message = []
    for c in encoded_textblock:
        if c.isalpha():
            temp = c.upper()
            idx_to_add = encode_alphabet.index(temp)
            decoded_message.append(candidate_cipher_alphabet[idx_to_add])
        else:
            decoded_message.append(c)
    decoded_message_str = ''.join(decoded_message)
    return decoded_message_str

def ngram_fitness(n, encoded_textblock, candidate_cipher_alphabet):
    decoded_message_str = decoded_message(encoded_textblock, candidate_cipher_alphabet)
    n_grams = []
    for i in range(len(decoded_message_str)-n+1):
        adder = decoded_message_str[i:i+n]
        if adder.isalpha():
            n_grams.append(adder)
        else:
            continue
    fitness_score = 0
    for n_gram in n_grams:
        freq = d.get(n_gram)
        if freq is not None:
            fitness_score+=log(freq, 2)
    return fitness_score

def hill_climbing(encoded_message):
    candidate_cipher_alphabet = ''.join(random.sample(encode_alphabet,len(encode_alphabet)))
    fitness_score = ngram_fitness(3, str_txt, candidate_cipher_alphabet)
    isTrue = True
    max_list = [fitness_score]
    while isTrue:
        idx1 = random.randint(0, len(encode_alphabet)-1)
        idx2 = random.randint(0, len(encode_alphabet)-1)
        c = list(candidate_cipher_alphabet)
        c[idx1], c[idx2] = c[idx2], c[idx1]
        new_candidate_cipher_alphabet = ''.join(c)
        fitness_score = ngram_fitness(3, str_txt, new_candidate_cipher_alphabet)
        if fitness_score>max(max_list):
            candidate_cipher_alphabet = new_candidate_cipher_alphabet
            max_list.append(fitness_score)
            print(decoded_message(str_txt, candidate_cipher_alphabet))
            input()
        else:
            continue

def genetic_alg(encoded_textblock, population_n):
    fitness_score_values = {}
    next_gen = []
    if population_n is None:
        population = []
        for i in range(0, POPULATION_SIZE):
            candidate_cipher_alphabet = ''.join(random.sample(encode_alphabet,len(encode_alphabet)))
            if candidate_cipher_alphabet not in population:
                population.append(candidate_cipher_alphabet)
        for p in population:
            fitness_score_values.update({p:ngram_fitness(3, encoded_textblock, p)})
    else:
        for p in population_n:
            fitness_score_values.update({p:ngram_fitness(3, encoded_textblock, p)})
    max_key = max(fitness_score_values, key=fitness_score_values.get)
    next_gen.append(max_key)
    dict_of_new_gen = {
        max_key: fitness_score_values.get(max_key)
    }
    while len(next_gen)!=POPULATION_SIZE:
        #Selection Method
        tournaments = []
        for n in range(0, 2*TOURNAMENT_SIZE):
            if population_n is not None:
                tournaments.append(random.choice(population_n))
            else:
                tournaments.append(random.choice(population))
        length = len(tournaments)
        middle_index = length//2
        tournament1 = tournaments[:middle_index]
        tournament2 = tournaments[middle_index:]
        tournament1_ranked = []
        temp_1 = []
        for t1 in tournament1:
            temp_1.append(fitness_score_values.get(t1))
        temp_1 = sorted(temp_1,reverse=True)
        parent_1 = None
        while parent_1 is None:
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                key_list = list(fitness_score_values.keys())
                val_list = list(fitness_score_values.values())
                position = val_list.index(temp_1[0])
                parent_1 = key_list[position]
            temp_1.pop(0)
        temp_2 = []
        for t2 in tournament2:
            temp_2.append(fitness_score_values.get(t2))
        temp_2 = sorted(temp_2,reverse=True)
        parent_2 = None
        while parent_2 is None:
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                key_list = list(fitness_score_values.keys())
                val_list = list(fitness_score_values.values())
                position = val_list.index(temp_2[0])
                parent_2 = key_list[position]
            temp_2.pop(0)
        #Breeding Process
        child_t = [None] * 26
        crossover_locations = random.sample(range(0,len(parent_1)-1), CROSSOVER_LOCATIONS)
        for random_crossover in crossover_locations:
            child_t[random_crossover] = parent_1[random_crossover]
        for c in parent_2:
            if None not in child_t:
                break
            if c not in child_t:
                length = len(child_t)
                i = 0
                while i<length:
                    if child_t[i] is None:
                        child_t[i] = c
                        break
                    i+=1
        child = ''.join(child_t)
        new_child = None
        if random.random() < MUTATION_RATE:
            idx1 = random.randint(0, len(child)-1)
            idx2 = random.randint(0, len(child)-1)
            c = list(child)
            c[idx1], c[idx2] = c[idx2], c[idx1]
            new_child = ''.join(c)
        if new_child is not None:
            if new_child not in next_gen:
                next_gen.append(new_child)
                dict_of_new_gen.update({new_child: ngram_fitness(3, encoded_textblock, new_child)})
        else:
            if child not in next_gen:
                next_gen.append(child)
                dict_of_new_gen.update({child: ngram_fitness(3, encoded_textblock, child)})
    max_key = max(dict_of_new_gen, key=dict_of_new_gen.get)
    return next_gen, dict_of_new_gen

start = time.perf_counter()
encoded_textblock = sys.argv[1]
generation, dict_of_new_gen = genetic_alg(encoded_textblock, None)
for i in range(0, 500):
    generation, dict_of_new_gen = genetic_alg(encoded_textblock, generation)
    max_key = max(dict_of_new_gen, key=dict_of_new_gen.get)
    #print(decoded_message(encoded_textblock, max_key))
    print(decoded_message(encoded_textblock, max_key), dict_of_new_gen.get(max_key))
    print()
    #input()
end = time.perf_counter()
#print(end-start)