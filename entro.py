#! /usr/local/bin/python
import re
from collections import Counter
from math import log

def build_freq_from_file(filename):
    letter_freq = Counter()
    with open(filename,'r') as input_file:
        not_letters_n_space = re.compile("[^a-z ]+")
        for line in input_file:
            lower_case_line = line.strip().lower()
            for letter in re.sub(not_letters_n_space, '', lower_case_line):
                letter_freq[letter] += 1
    input_file.close()
    return letter_freq

def calculate_entropy_from_freq(rel_freq):
    total = sum(rel_freq.values()) + 0.0
    probabilities = {}
    entropy = 0
    for letter in rel_freq:
        probabilities[letter] = rel_freq[letter]/total
        entropy += probabilities[letter] * log(probabilities[letter],2) 
    return -entropy

def kl_divergence(entropy, cross_entropy):
    # Kullback-Leibler divergence is a measure of how different two probability
    # distributions are.
    return cross_entropy - entropy

def calculate_cross_entropy_from_freqs(freq_a, freq_b):
    total_a = sum(freq_a.values()) + 0.0
    total_b = sum(freq_b.values()) + 0.0
    cross_entropy = 0.0
    for letter in freq_b:
        try:
            cross_entropy += freq_a[letter] / total_a *  \
                log(freq_b[letter] / total_b, 2)
        except ValueError :
            cross_entropy += 0.0
    return -cross_entropy

if __name__ == '__main__':
    #AiW is egutenberg version of Alice in Wonderland
    aiw_entropy = calculate_entropy_from_freq(build_freq_from_file("AiW.txt"))
    #AoSH is egutenberg version of Adventures of Sherlock Holmes
    print calculate_entropy_from_freq(build_freq_from_file("AoSH.txt"))

    aiw_aosh_cross_entropy = calculate_cross_entropy_from_freqs(build_freq_from_file("AiW.txt"), \
            build_freq_from_file("AoSH.txt"))

    print kl_divergence(aiw_entropy, aiw_aosh_cross_entropy)
