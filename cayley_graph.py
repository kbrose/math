import sys

generators = ['a','b']
relators = [['a',2],['b',5],['ab',3],['1',1]]
tab = '    '
MAX_RECURSE_LEVELS = 100

outfile = open('graph1.dot','w')

#simplifies element given relations
def simplify(elem,rels):
    #TODO: allow this to handle cases like (ab)^2(b^3)
    #TODO: allow this to set relators equal to other than 1
    relators = [r[0]*r[1] for r in rels]
    change_made = True
    while change_made:
        change_made = False
        #TODO: make this dynamic programming solution
        for i in range(len(elem)):
            for rel in relators:
                if elem[i:i+len(rel)] == rel:
                    change_made = True
                    elem = elem[:i] + elem[i+len(rel):]
    if elem == '':
        return '1'
    return elem

#print simplify('bbbbab',relators)
#quit()

def draw_cayley(gens,rels):
    to_visit = [['1',0]] # [element, recurse_level]
    have_visited = set()
    while to_visit != []:
        curr_pair = to_visit.pop() #order does not matter
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
        have_visited.add(simplify(curr,rels))

#returns relators along with all their inverses, and 1.
def expand_relators(gens,rels):
    for gen in gens:
        if not gen in [rel[0] for rel in rels]:
            sys.stderr.write("Not a finite group! Generator \"" + 
                             gen + "\" was not given an order.\n")
            quit()
    ret = []
    for rel in rels:
        if rels[1] > 2:
            ret.append([simplify(inverse(gens,rels,rel[0]),rels), rel[1]])
    ret += rels
    return ret

def inverse(gens,rels,elem):
    elem = elem[::-1] # reverse
    ret = ''
    for c in elem:
        order = rels[[r[0] for r in rels].index(c)][1] # ugh. make it a dict already
        ret = ret + c*(order-1)
    return ret


if __name__ == '__main__':
    outfile.write('digraph G {\n')
    relators = expand_relators(generators,relators)
    print relators
#    quit()
    draw_cayley(generators,relators)
    outfile.write('}\n')            

