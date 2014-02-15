from math import log
import matplotlib.pyplot as plt

### prints the initial distributions as described in write-up
def show_init(A,B,Pi,states,out_file):
    out_file.write( '---------------------------------\n')
    out_file.write( '-  Initialization               -\n')
    out_file.write( '---------------------------------\n')
    for i in states:
        out_file.write( 'Creating State ' + str(i) + '\n')

        # transitions
        out_file.write( 'Transitions\n')
        for j in states:
            out_file.write( '     To state  ' + str(j) + ' ' + '%.4g\n' % A[i][j])
        
        # emissions
        out_file.write('\nEmission probabilities\n')
        emission_sum = 0.0
        letters = sorted(B[i].items(), key=lambda x: x[1], reverse=True)
        for letter in letters:
            emission_sum += letter[1]
            out_file.write('     Letter    ' + letter[0] + '  %.4g\n' % letter[1])
        out_file.write('     Total: %.4g\n\n' % emission_sum)

    # Pi
    out_file.write('\n')
    out_file.write('---------------------------------\n')
    out_file.write('Pi:\n')
    for i in states:
        out_file.write('     State  ' + str(i) + '     %.4g\n\n\n' % Pi[i])

def init_alpha_beta(Pi,word,out_file):
    out_file.write('*** word: %s ***\n' % word)
    for i in range(len(Pi)):
        out_file.write('Pi of  ' + str(i) + '  %.4g\n' % Pi[i])

def gorey_alpha(t,char,to_sum_list,out_file):
    out_file.write('\ttime ' + str(t) + ': \'' + char + '\'\n')
    for to_state in range(len(to_sum_list)):
        out_file.write('\t\tto state: ' + str(to_state) + '\n')
        for from_state in range(len(to_sum_list[to_state])):
            out_file.write('\t\t\tfrom state   ' + str(from_state))
            out_file.write('  Alpha: %.4g\n' % to_sum_list[to_state][from_state])

def show_alpha_beta(name,a_or_b,out_file):
    out_file.write(name + ':\n')

    curr_max_len = 0
    for t in range(len(a_or_b)):
        for state in range(len(a_or_b[t])):
            curr_max_len = max(curr_max_len,len('%.4g' % a_or_b[t][state]))
    curr_max_len += 2
    for t in range(len(a_or_b)):
        to_concat = ' '
        for state in range(len(a_or_b[t])):
            to_concat += 'State ' + str(state)
            to_concat += ' '*(curr_max_len - len('%.4g' % a_or_b[t][state]))
            to_concat += ('%.4g' % a_or_b[t][state]) + '    '
        out_file.write('\tTime  ' + str(t) + ':   ' + to_concat + '\n')
    out_file.write('\n')

def sum_of_probs(s,iter,out_file):
    out_file.write('Iteration %d\n' % (iter + 1))
    out_file.write('Sum of probabilities: %.4g\n\n' % s)

def init_soft(out_file):
    out_file.write('---------------------------\n')
    out_file.write('Soft counts\n')
    out_file.write('---------------------------\n')

def soft_count(letter,count,states,out_file):
    out_file.write('\tLetter: ' + letter + '\n')
    s = 0.0
    for from_state in states:
        out_file.write('\t\tFrom state: ' + str(from_state) + '\n')
        for to_state in states:
            s += count[from_state][to_state]
            out_file.write('\t\t\tTo state: ' + str(to_state) + 
                           '  ' + '%.4g\n' % count[from_state][to_state])
    # out_file.write('\t\tSum: ' + '%.4g\n' % s)

def init_emissions(out_file):
    out_file.write('Calculating new Emissions:\n')

def from_state_output(from_state,out_file):
    out_file.write('\n\tFrom State: ' + str(from_state) + '\n')

def letter_prob(B,states,out_file):
    out_file.write('Letter probabilities:\n')
    for i in states:
        out_file.write('\tFrom state: ' + str(i) + '\n')
        letters = sorted(B[i].items(), key=lambda x: x[1], reverse=True)
        for letter in letters:
            out_file.write('\t\tLetter \'' + letter[0] + '\': %.4g\n' % letter[1])

domain_fixer = 0.0000001

def other_states_prob(B,i,letter,states):
    other_states = 0.0
    for j in states:
        if j == i:
            continue
        other_states += B[j][letter]
    if other_states == 0.0:
        return domain_fixer # fixes divide by 0
    return other_states

def log_letter_prob(B,states,out_file):
    out_file.write('State Divisions:\n')
    for i in states:
        out_file.write('\tAssigned to state ' + str(i) + ':\n')
        letters = sorted(B[i].items(), key=lambda x: log((x[1] + domain_fixer) / other_states_prob(B,i,x[0],states)), reverse=True)
        above_0 = filter(lambda x: log((x[1] + domain_fixer) / other_states_prob(B,i,x[0],states)) >= 0, B[i].items())
        for letter in letters:
            if letter in above_0: # inefficient, but only done once per program
                out_file.write('\t\tLetter \'' + letter[0] + '\': %.4g\n' % letter[1])

def max_trans(out_file):
    out_file.write('\nCalculating new transitions:\n')

def new_A_output(to_state,prev,new,normalizer,out_file):
    out_file.write('\t\tTo state:   ' + str(to_state) + 
                   ' prob: %.4g (%.4g over %.4g)\n' % (new,prev,normalizer))

def A_output(A,states,out_file):
    out_file.write('\nTransition Probabilities:')
    for from_state in states:
        from_state_output(from_state,out_file)
        for to_state in states:
            out_file.write('\t\tTo state:   ' + str(to_state) + 
                           ' prob: %.4g\n' % (A[from_state][to_state]))

def max_Pi(out_file):
    out_file.write('\nCalculating new Pi:\n')

def show_Pi(Pi,out_file):
    out_file.write('\nPi values:\n')
    for state in range(len(Pi)):
        out_file.write('\tState  ' + str(state) + '   %.4g\n' % Pi[state])

def init_viterbi(delta,word,states,out_file):
    out_file.write('----------------------------\n')
    out_file.write('      Viterbi Path \n')
    out_file.write('----------------------------\n')
    out_file.write(word + '\n\n')
    for i in states:
        out_file.write('Delta[1] of state ' + str(i) + ': ' + str(delta[i][0]) + '\n')
    out_file.write('\n')

def viterbi_time(t,l,out_file):
    out_file.write('Time ' + str(t) + ': letter ' + l + '\n')

def viterbi_step(come_from,s,t,themax,states,out_file):
    out_file.write('\tat state ' + str(s) + ':\n')
    for state in states:
        out_file.write('\t\tfrom state ' + str(state) + ': %.4g\n' % come_from[state][0])
    out_file.write('\tbest to come from ' + str(themax[1]) + ' (at %.4g)\n\n' % themax[0])

def viterbi_path(path,out_file):
    out_file.write('Viterbi path:\n')
    out_file.write('time :')
    for t in range(len(path)):
        out_file.write('\t' + str(t))
    out_file.write('\n')
    out_file.write('state:')
    for t in range(len(path)):
        out_file.write('\t' + str(path[t]))
    out_file.write('\n')

def Plot2D(data,sum_of_probs,sum_of_probs_list,out_file):
    x = [d[0] for d in data]
    y = [d[1] for d in data]
    min_val = min(sum_of_probs_list)
    max_val = max(sum_of_probs_list)
    fixed_probs = [(p - min_val) / (max_val - min_val) for p in sum_of_probs_list]
    colors = plt.cm.coolwarm(fixed_probs)

    plt.scatter(x,y,c=colors,edgecolors=colors,s=30,marker='+')

    plt.xlabel('Transition from 0 to 1')
    plt.ylabel('Transition from 1 to 0')
    plt.title('Transition probabilities - total probability of %.4g' % sum_of_probs)
    plt.xlim(0,1)
    plt.ylim(0,1)

    plt.savefig(out_file)
    plt.close()










