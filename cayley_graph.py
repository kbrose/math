import sys

generators = ['a','b']
relators = [['a',2],['b',5],['ab',3]]
tab = '    '
MAX_RECURSE_LEVELS = 100

out_file = open('graph1.dot','w')

#simplifies element given relations
def simplify(elem,rels):
    #TODO: allow this to handle cases like (ab)^2(b^3)
    is_id = [r[0]*r[1] for r in rels]
    

def draw_cayley(gens,rels):
    for gen in gens:
        if not gen in [rel[0] for rel in rels]:
            sys.stderr.write("Not a finite group! Generator \"" + 
                             gen + "\" was not given an order.\n")
    to_visit = [''] #corresponds to identity in group
    have_visited = set()
    while to_visit != []:
        curr = to_visit.pop() #order does not matter
        for gen in gens:
            prod = curr + gen #product corresponds to string concat
            prod = simplify(prod)
            outfile.write(tab + curr + '->' + prod + 
                          ' [label="' + gen + '"')
            if not prod in have_visited:
                have_visited.add(prod)

draw_cayley(generators, relators)

