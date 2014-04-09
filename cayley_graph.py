import sys
from knuth_bendix import knuth_bendix

#TODO: Use subgraphs with attribute edge [dir=none]
#      to allow for undirected edges

generators = ['a','b']
relators = [['a',2,'',0],['b',5,'',0],['ab',3,'',0]]

outfile = open('graph1.dot','w')
class cayley_graph:
    def __init__(self,gens,rels,max_recurse):
        self.kb = knuth_bendix(rels,500)
        self.gens = gens
        self.MAX_RECURSE_LEVELS = max_recurse
        self.tab = '    '

    def simplify(self,elem):
        return self.kb.reduce_all(elem)

    def draw_cayley(self,writefile):
        to_visit = [['',0]] # [element, recurse_level]
        have_visited = set()
        while to_visit != []:
            curr_pair = to_visit.pop() #order does not matter
            curr = curr_pair[0]
            if curr == 'aababbbab':
                print 'here 2'
            if curr_pair[1] > self.MAX_RECURSE_LEVELS:
                sys.stderr.write("Reached maximum recursion depth, stopping.\n")
                quit()
            for gen in self.gens:
                prod = curr + gen #product corresponds to string concat
                prod = self.simplify(prod)
                if curr == '':
                    outfile.write(self.tab + '1' + ' -> ' + prod + 
                                ' [label="' + gen + '"]\n')
                elif prod == '':
                    outfile.write(self.tab + curr + ' -> ' + '1' + 
                                ' [label="' + gen + '"]\n')
                else:
                    outfile.write(self.tab + curr + ' -> ' + prod + 
                                ' [label="' + gen + '"]\n')
                if not prod in ([x[0] for x in to_visit] + list(have_visited)):
                    to_visit.append([prod,curr_pair[1] + 1])
            have_visited.add(curr)


if __name__ == '__main__':
    outfile.write('digraph G {\noverlap=scale\n')
    c = cayley_graph(generators,relators,100)
    c.draw_cayley(outfile)
    outfile.write('}\n')     

