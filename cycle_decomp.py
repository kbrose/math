### EXAMPLES:
### > (i j k)^2
### (i k j)
### > (1 2 3 4 5)(5 3 1)(2 4)
### (1 4 3 2)

import sys

def decomp(done, cycles):
    concat_cycles = reduce(lambda x,y: x+y, cycles)
    i = 0
    while i < len(concat_cycles) and concat_cycles[i] in done:
        i += 1
    if i == len(concat_cycles):
        return []
    symbol = concat_cycles[i]
    done, res = get_from_cycles(done, symbol, cycles)
    if len(res) == 1:
        return decomp(done, cycles)
    else:
        return [res] + decomp(done, cycles)

def get_from_cycles(done, sym, cycles):
    res = []
    while sym not in done:
        done += [sym]
        res += [sym]
        for cycle in cycles:
            if sym in cycle:
                index = cycle.index(sym)
                sym = cycle[(index + 1) % (len(cycle))]
    return done, res

def format(s):
    total = []
    curr = []
    curr_sym = ''
    i = 0
    while i < len(s):
        if s[i]== '(':
            curr = []
        elif s[i]== ')':
            if curr_sym != '':
                curr += [curr_sym]
                curr_sym = ''
            total += [curr]
        elif s[i]== ' ' and curr_sym != '':
            curr += [curr_sym]
            curr_sym = ''
        elif s[i]== '^':
            i += 1
            start = i
            while i < len(s) and s[i].isdigit():
                i += 1
            end = i
            i -= 1
            power = int(s[start:end])
            total += [curr]*(power - 1)
        else:
            curr_sym += s[i]
        i += 1
    return total

def show_decomp(cycles):
    if len(cycles) == 0:
        sys.stdout.write('Identity')
    for cycle in cycles:
        sys.stdout.write('(')
        for sym in cycle:
            print sym,
        sys.stdout.write(')')
    print ''

def main():
    i = raw_input('> ')
    if i in ['quit', 'q']:
        quit()
    cycles = format(i)
    show_decomp(decomp([],cycles))
    main()

if __name__ == '__main__':
    print 'Type \"q\" or \"quit\" to quit.'
    main()


