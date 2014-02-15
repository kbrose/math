import sys
import random
import output
import os
import output

class HMM:
    ### takes a list of letters and the number of states
    ### and returns the initial distibutions A, B, and Pi
    def __init__(self, letters, words, states, out, out_pdf, VERBOSE_FLAG):
        # transition probabilities
        self.A = [[0 for i in states] for i in states]
        for i in states:
            transition_total = 0.0 
            for j in states:
                rand = random.uniform(0,1.0)
                transition_total += rand
                self.A[i][j] = rand
            for j in states:
                self.A[i][j] = self.A[i][j] / transition_total
        # A[i][j] is the transition probability for i -> j

        # emission probabilities
        self.B = [{} for i in states]
        for i in states:
            emission_total = 0.0
            for letter in letters:
                rand = random.uniform(0,1.0)
                emission_total += rand
                self.B[i][letter] = rand
            for letter in letters:
                self.B[i][letter] = self.B[i][letter] / emission_total
        # B[i][letter] is the probability state i emits the given letter

        # initial state distribution    
        self.Pi = [0 for i in states]
        pi_total = 0.0
        for i in states:
            rand = random.uniform(0,1.0)
            pi_total += rand
            self.Pi[i] = rand
        for i in states:
            self.Pi[i] = self.Pi[i] / pi_total

        # other initializers
        self.counts = {}
        self.states = states
        self.out = out
        self.out_pdf = out_pdf
        self.words = words
        self.sum_of_probs = 0.0
        self.sum_of_probs_list = [0.0]
        self.trans_list = []
        self.VERBOSE_FLAG = VERBOSE_FLAG

        #if self.VERBOSE_FLAG:
        output.show_init(self.A,self.B,self.Pi,self.states,self.out)

    ### Computes forward and backward according to
    ### appropriate formulas.
    def forward_backward(self,word):
        if self.VERBOSE_FLAG:
            output.init_alpha_beta(self.Pi,word,self.out)
        T = len(word)
        alpha = [[0 for i in self.states] for i in range(T+1)]
        beta = [[0 for i in self.states] for i in range(T+1)]
        # alpha[t][s] gives alpha for time t and state s
        # similarly for beta[t][s]
        alpha[0] = self.Pi
        beta[T] = [1.0 for i in self.states]
        for t in range(1,T+1):
            if self.VERBOSE_FLAG:
                to_sum_list = []
            for s in self.states:
                to_sum = [alpha[t-1][j] * self.A[j][s] * self.B[j][word[t-1]] 
                          for j in self.states]
                alpha[t][s] = sum(to_sum)
                if self.VERBOSE_FLAG:
                    to_sum_list.append(to_sum)
                to_sum = [beta[T-t+1][j] * self.A[s][j] * self.B[s][word[T-t]] 
                          for j in self.states]
                beta[T-t][s] = sum(to_sum)
            if self.VERBOSE_FLAG:
                output.gorey_alpha(t+1,word[t-1],to_sum_list,self.out)
        if self.VERBOSE_FLAG:
            output.show_alpha_beta('alpha', alpha, self.out)
            output.show_alpha_beta('beta', beta, self.out)
        return alpha, beta

    ### computes the soft count of the given word, i.e.
    ###                     alpha[t][i]*A[i][j]*B[i][word[t]]*beta[t+1][j]
    ### counts[t][i][j] =  ------------------------------------------------
    ###                    probability of whole word = sum_j(alpha[T-1][j])
    def soft_count(self,word):
        if self.VERBOSE_FLAG:
            output.init_soft(self.out)

        # squelch output
        temp = self.VERBOSE_FLAG
        self.VERBOSE_FLAG = 0
        alpha,beta = self.forward_backward(word)
        self.VERBOSE_FLAG = temp

        prob_of_word = sum(alpha[len(alpha) - 1])
        counts = [[[0 for i in self.states] 
                      for j in self.states] 
                      for letter in word]
        # counts[t][i][j] is the count of i to j at time t
        for t in range(len(word)):
            for i in self.states:
                for j in self.states:
                    al_it = alpha[t][i]
                    a_ij = self.A[i][j]
                    b_it = self.B[i][word[t]]
                    be_jt = beta[t+1][j]
                    counts[t][i][j] = al_it * a_ij * b_it * be_jt / prob_of_word
            if self.VERBOSE_FLAG:
                output.soft_count(word[t],counts[t],self.states,self.out)
        return counts

    def maximize_emission(self):
        new_B = [{} for i in self.states]
        # new_B[state][letter] gives TOTAL soft count
        # for given letter FROM given state
        for word in self.words:
            count = self.counts[word]
            for t in range(len(word)):
                for from_state in self.states:
                    if word[t] in new_B[from_state]:
                        to_sum = [count[t][from_state][to_state] 
                                  for to_state in self.states]
                        new_B[from_state][word[t]] += sum(to_sum)
                    else:
                        to_sum = [count[t][from_state][to_state] 
                                  for to_state in self.states]
                        new_B[from_state][word[t]] = sum(to_sum)
        if self.VERBOSE_FLAG:
            output.init_emissions(self.out)
        normalizers = []
        for from_state in self.states:
            normalizer = sum(new_B[from_state].values())
            normalizers.append(normalizer)
            for letter in new_B[from_state].keys():
                new_B[from_state][letter] = new_B[from_state][letter] / normalizer
        if self.VERBOSE_FLAG:
            output.letter_prob(new_B,self.states,self.out)
        return new_B, normalizers

    def maximize_transition(self,normalizers):
        if self.VERBOSE_FLAG:
            output.max_trans(self.out)
        new_A = [[0 for i in self.states] for i in self.states]
        for word in self.words:
            count = self.counts[word]
            for i in self.states:
                for j in self.states:
                    for time in count:
                        new_A[i][j] += time[i][j]
        for from_state in self.states:
            if self.VERBOSE_FLAG:
                output.from_state_output(from_state,self.out)
            for to_state in self.states:
                curr = new_A[from_state][to_state]
                new_A[from_state][to_state] = curr / normalizers[from_state]
                if self.VERBOSE_FLAG:
                    output.new_A_output(to_state,curr,new_A[from_state][to_state],
                                        normalizers[from_state],self.out)
        return new_A

    def maximize_Pi(self):
        if self.VERBOSE_FLAG:
            output.max_Pi(self.out)
        new_Pi = [0 for i in self.states]
        for word in self.words:
            count = self.counts[word]
            for i in self.states:
                for j in self.states:
                    new_Pi[i] += count[0][i][j]
        Z = len(self.words)
        for state in self.states:
            new_Pi[state] = new_Pi[state] / Z
        if self.VERBOSE_FLAG:
            output.show_Pi(new_Pi,self.out)
        return new_Pi

    ### Calculates the viterbi path through a given word.
    ### The viterbi path is the path through the HMM
    ### with the highest probability.
    def viterbi(self, word):
        T = len(word)
        # delta[i][t] gives delta for state i at time t
        delta = [[0 for t in range(T+1)] for s in self.states]
        # backtrace[j][t] gives the state i that most likely
        # leads to state j at time t
        backtrace = [[0 for t in range(T+1)] for s in self.states]
        for i in self.states:
            delta[i][0] = self.Pi[i]
        if self.VERBOSE_FLAG:
            output.init_viterbi(delta,word,self.states,self.out)
        for t in range(1,T+1):
            if self.VERBOSE_FLAG:
                output.viterbi_time(t,word[t-1],self.out)
            for i in self.states:
                prev_res = [(delta[j][t-1] * self.A[j][i] * self.B[j][word[t-1]],j) 
                            for j in self.states]
                themax = max(prev_res)
                delta[i][t] = themax[0]
                backtrace[i][t] = themax[1]
                if self.VERBOSE_FLAG:
                    output.viterbi_step(prev_res,i,t,themax,self.states,self.out)
        final_path = [0 for i in range(T+1)]
        final_prob, final_path[T] = (max([(delta[j][T],j) for j in self.states]))
        for t in range(T-1,-1,-1):
            final_path[t] = backtrace[final_path[t+1]][t+1]
        if self.VERBOSE_FLAG:
            output.viterbi_path(final_path,self.out)
        return final_prob, final_path

    ### cycles through the HMM until one of the given stop
    ### condition causes it to, well, stop.
    def cycle(self,max_iters,min_change):
        self.trans_list = [(self.A[0][1],self.A[1][0])]
        for i in range(max_iters):
            sum_of_probs = 0.0
            for word in self.words:
                alpha, unused_beta = self.forward_backward(word)
                sum_of_probs += sum(alpha[len(alpha)-1])
            if self.VERBOSE_FLAG:
                output.sum_of_probs(sum_of_probs,i,self.out)

            diff = sum_of_probs - self.sum_of_probs
            if diff < min_change:
                break
            self.sum_of_probs = sum_of_probs
            self.sum_of_probs_list.append(self.sum_of_probs)

            for word in self.words:
                self.counts[word] = self.soft_count(word)

            new_B_values, normalizers = self.maximize_emission()
            new_A_values = self.maximize_transition(normalizers)
            new_Pi_values = self.maximize_Pi()
            self.B = new_B_values
            self.A = new_A_values
            self.Pi = new_Pi_values
            self.trans_list.append((self.A[0][1],self.A[1][0]))

        if self.VERBOSE_FLAG:
            output.letter_prob(self.B,self.states,self.out)
        output.log_letter_prob(self.B,self.states,self.out)
        output.A_output(self.A,self.states,self.out)
        output.show_Pi(self.Pi,self.out)
        output.sum_of_probs(sum_of_probs,i,self.out)

    def make_plot(self):
        output.Plot2D(self.trans_list, self.sum_of_probs, self.sum_of_probs_list, self.out_pdf)

