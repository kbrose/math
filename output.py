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

def sum_of_probs(s,out_file):
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
            out_file.write('\t\t\tTo state: ' + str(to_state) + '  ' + '%.4g\n' % count[from_state][to_state])
    # out_file.write('\t\tSum: ' + '%.4g\n' % s)

def init_emissions(out_file):
    out_file.write('Calculating new Emissions:\n')

def from_state_output(from_state,out_file):
    out_file.write('\n\tFrom State: ' + str(from_state) + '\n')

def letter_prob(B,states,out_file):
    for i in states:
        out_file.write('\tFrom state: ' + str(i) + '\n')
        letters = sorted(B[i].items(), key=lambda x: x[1], reverse=True)
        for letter in letters:
            out_file.write('\t\tLetter \'' + letter[0] + '\': %.4g\n' % letter[1])

def max_trans(out_file):
    out_file.write('\nCalculating new transitions:\n')

def new_A_output(to_state,prev,new,normalizer,out_file):
    out_file.write('\t\tTo state:   ' + str(to_state) + 
                   ' prob: %.4g (%.4g over %.4g)\n' % (new,prev,normalizer))

def max_Pi(out_file):
    out_file.write('\nCalculating new Pi:\n')

def show_Pi(Pi,out_file):
    for state in range(len(Pi)):
        out_file.write('\tState  ' + str(state) + '   %.4g\n' % Pi[state])

