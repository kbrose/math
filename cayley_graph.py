import sys
import word_problem.simplify

generators = ['a','b']
relators = dict([['a',2,'',0],['b',5,'',0],['ab',3,'',0]])
tab = '    '
MAX_RECURSE_LEVELS = 100

outfile = open('graph1.dot','w')

def draw_cayley(gens,rels):
    to_visit = [['1',0]] # [element, recurse_level]
    have_visited = set()
    while to_visit != []:
        curr_pair = to_visit.pop() #order does not matter
        have_visited.add(simplify(curr,rels))
        curr = curr_pair[0]
        if curr_pair[1] > MAX_RECURSE_LEVELS:
            #print curr_pair[0]
            #print len(have_visited)
            sys.stderr.write("Reached maximum recursion depth, stopping.\n")
            quit()
        for gen in gens:
            prod = curr + gen #product corresponds to string concat
            prod = simplify(prod,rels)
            outfile.write(tab + curr + ' -> ' + prod + 
                          ' [label="' + gen + '"]\n')
            if not (prod in to_visit or prod in have_visited):
                print curr, prod, curr_pair[1]
                to_visit.append([prod,curr_pair[1] + 1])


if __name__ == '__main__':
    outfile.write('digraph G {\n')
    draw_cayley(generators,relators)
    outfile.write('}\n')            

