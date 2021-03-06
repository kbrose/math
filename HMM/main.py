import sys
import random
import output
import os
from HMM import HMM

NUMBER_OF_STATES = 2
STATES = [i for i in range(NUMBER_OF_STATES)]
VERBOSE_FLAG = 0
MAX_ITERS = 15
MIN_CHANGE = -100
#MIN_CHANGE = .00000000001

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

### A  - transition probabilities
### B  - emission probailities
### Pi - initial state distribution
if __name__ == '__main__':
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print 'usage: HMM.py <input_file> <out_text> <out_png> [-v]'
        quit()
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    out_pdf_name = sys.argv[3]
    if len(sys.argv) == 5:
        if sys.argv[4] != '-v':
            print 'usage: python HMM.py <input_file> <out_text> <out_png> [-v]'
            quit()
        VERBOSE_FLAG = 1
    letters, words = read_in(input_file_name)
    with open(output_file_name,'w') as out_text:
        myHMM = HMM(letters,words,STATES,out_text,out_pdf_name,VERBOSE_FLAG)
        myHMM.cycle(MAX_ITERS,MIN_CHANGE)
        myHMM.make_plot()

