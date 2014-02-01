import sys
import random
import output
import os

NUMBER_OF_STATES = 2
STATES = [i for i in range(NUMBER_OF_STATES)]
VERBOSE_FLAG = 0

### reads in a file, creating a sorted list of letters
### and words with an appended #.
def read_in(file_name):
    letters = {}
    words = {}
    with open(file_name) as f:
        for line in f:
            ls = line.split()
            for word in ls:
                new_word = word + '#'
                for letter in new_word:
                    if letter not in letters:
                        letters[letter] = 1
                if new_word not in words:
                    words[new_word] = 1
    return sorted(letters.keys()), sorted(words.keys())

### takes a list of letters and the number of states
### and returns the initial distibutions A, B, and Pi
def init_probs(letters, states):
    # transition probabilities
    A = [[0 for i in states] for i in states]
    for i in states:
        transition_total = 0.0 
        for j in states:
            rand = random.uniform(0,1.0)
            transition_total += rand
            A[i][j] = rand
        for j in states:
            A[i][j] = A[i][j] / transition_total
    # A[i][j] is the transition probability for i -> j

    # emission probabilities
    B = [{} for i in states]
    for i in states:
        emission_total = 0.0
        for letter in letters:
            rand = random.uniform(0,1.0)
            emission_total += rand
            B[i][letter] = rand
        for letter in letters:
            B[i][letter] = B[i][letter] / emission_total

    # initial state distribution    
    Pi = [0 for i in states]
    pi_total = 0.0
    for i in states:
        rand = random.uniform(0,1.0)
        pi_total += rand
        Pi[i] = rand
    for i in states:
        Pi[i] = Pi[i] / pi_total

    return A, B, Pi

def forward_backward(A,B,Pi,word,states,out):
    if VERBOSE_FLAG:
        output.init_alpha_beta(Pi,word,out)
    T = len(word)
    alpha = [[0 for i in states] for i in range(T+1)]
    beta = [[0 for i in states] for i in range(T+1)]
    # alpha[t][s] gives alpha for time t and state s
    # similarly for beta
    alpha[0] = Pi
    beta[T] = [1.0 for i in states]
    for t in range(1,T+1):
        if VERBOSE_FLAG:
            to_sum_list = []
        for s in states:
            to_sum = [alpha[t-1][j] * A[j][s] * B[j][word[t-1]] 
                      for j in states]
            alpha[t][s] = sum(to_sum)
            if VERBOSE_FLAG:
                to_sum_list.append(to_sum)
            to_sum = [beta[T-t+1][j] * A[s][j] * B[s][word[T-t]] 
                      for j in states]
            beta[T-t][s] = sum(to_sum)
        if VERBOSE_FLAG:
            output.gorey_alpha(t+1,word[t-1],to_sum_list,out)
    if VERBOSE_FLAG:
        output.show_alpha_beta('alpha', alpha, out)
        output.show_alpha_beta('beta', beta, out)
    return alpha, beta

def soft_count(A,B,Pi,word,states,out):
    if VERBOSE_FLAG:
       output.init_soft(out)
    f = open(os.devnull, 'w')
    alpha,beta = forward_backward(A,B,Pi,word,states,f)
    f.close() # write output to nothing even when verbose flag set
    prob_of_word = sum(alpha[len(alpha) - 1])
    counts = [[[0 for i in states] 
                  for j in states] 
                  for letter in word]
    # counts[t][i][j] is the count of i to j at time t
    for t in range(len(word)):
        for i in states:
            for j in states:
                alpha_it = alpha[t][i]
                a_ij = A[i][j]
                b_it = B[i][word[t]]
                beta_jt = beta[t+1][j]
                counts[t][i][j] = alpha_it * a_ij * b_it * beta_jt / prob_of_word
        if VERBOSE_FLAG:
            output.soft_count(word[t],counts[t],states,out)
    return counts

def maximize_emission(A,B,Pi,words,states,out):
    with open(os.devnull, 'w') as devnull:
        new_B = [{} for i in states]
        # new_B[state][letter] gives TOTAL soft count
        # for given letter FROM given state
        for word in words:
            count = soft_count(A,B,Pi,word,states,devnull)
            for t in range(len(word)):
                for from_state in states:
                    if word[t] in new_B[from_state]:
                        to_sum = [count[t][from_state][to_state] for to_state in states]
                        new_B[from_state][word[t]] += sum(to_sum)
                    else:
                        to_sum = [count[t][from_state][to_state] for to_state in states]
                        new_B[from_state][word[t]] = sum(to_sum)
        if VERBOSE_FLAG:
            output.init_emissions(out)
        normalizers = []
        for from_state in states:
            normalizer = sum(new_B[from_state].values())
            normalizers.append(normalizer)
            for letter in new_B[from_state].keys():
                new_B[from_state][letter] = new_B[from_state][letter] / normalizer
        if VERBOSE_FLAG:
            output.letter_prob(B,states,out)
    return new_B, normalizers

def maximize_transition(A,B,Pi,words,normalizers,states,out):
    with open(os.devnull, 'w') as devnull:
        if VERBOSE_FLAG:
            output.max_trans(out)
        new_A = [[0 for i in states] for i in states]
        for word in words:
            count = soft_count(A,B,Pi,word,states,devnull)
            for i in states:
                for j in states:
                    for time in count:
                        new_A[i][j] += time[i][j]
        for from_state in states:
            if VERBOSE_FLAG:
                output.from_state_output(from_state,out)
            for to_state in states:
                curr = new_A[from_state][to_state]
                new_A[from_state][to_state] = curr / normalizers[from_state]
                if VERBOSE_FLAG:
                    output.new_A_output(to_state,curr,new_A[from_state][to_state],
                                        normalizers[from_state],out)
    return new_A


def maximize_Pi(A,B,Pi,words,states,out):
    with open(os.devnull, 'w') as devnull:
        if VERBOSE_FLAG:
            output.max_Pi(out)
        new_Pi = [0 for i in states]
        for word in words:
            count = soft_count(A,B,Pi,word,states,devnull)
            for i in states:
                for j in states:
                    new_Pi[i] += count[0][i][j]
        Z = len(words)
        for state in states:
            new_Pi[state] = new_Pi[state] / Z
        if VERBOSE_FLAG:
            output.show_Pi(new_Pi,out)
    return new_Pi

### A  - transition probabilities
### B  - emission probailities
### Pi - initial state distribution
if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print 'usage: python HMM.py <input_file> <output_file> [-v]'
        quit()
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    if len(sys.argv) == 4:
        if sys.argv[3] != '-v':
            print 'usage: python HMM.py <input_file> <output_file> [-v]'
            quit()
        VERBOSE_FLAG = 1
    # PART 1
    letters, words = read_in(input_file_name)
    A, B, Pi = init_probs(letters,STATES)
    with open(output_file_name,'w') as out:
        if VERBOSE_FLAG:
            output.show_init(A,B,Pi,STATES,out)
        # PARTS 2 AND 3
        sum_of_probs = 0.0
        sum_of_probs2 = 0.0
        for word in words:
            alpha, unused_beta = forward_backward(A,B,Pi,word,STATES,out)
            sum_of_probs += sum(alpha[len(alpha)-1]) # PART 3
        if VERBOSE_FLAG:
            output.sum_of_probs(sum_of_probs,out)
        # PARTS 4 and 5.1
        new_B_values, normalizers = maximize_emission(A,B,Pi,words,STATES,out)
        # PART 5.2
        new_A_values = maximize_transition(A,B,Pi,words,normalizers,STATES,out)
        new_Pi_values = maximize_Pi(A,B,Pi,words,STATES,out)
        # B = new_B_values
        # A = new_A_values
        # Pi = new_Pi_values

