import sys
from knuth_bendix import knuth_bendix

#TODO: Use subgraphs with attribute edge [dir=none]
#      to allow for undirected edges

class cayley_graph:
    def __init__(self,gens,rels,max_recurse):
        self.kb = knuth_bendix(rels,100)
        self.gens = gens
        self.MAX_RECURSE_LEVELS = max_recurse
        self.tab = '    '

    def simplify(self,elem):
        return self.kb.simplify(elem)

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

#TODO: add capabilities for exponenets/complicated expressions
def process_relators(raw):
    raw = raw.replace(' ','')
    rels = raw.split(',')
    ret = []
    for rel in rels:
        if '=' in rel:
            idx = rel.index('=')
            before = rel[:idx]
            after = rel[idx+1:]
            ret.append([before,1,after,1])
        else:
            ret.append([rel,1,'',0])
    return ret

def usage():
    print "usage: python cayley_graph.py [-s] "
    print "                              [-o filename]"
    print "                              r1[=r1'],...,rm[=rm']"
    print "         where {ri} are the relators. It is assumed that ri=1 unless"
    print "         it is otherwise specified. The generators are assumed to be all"
    print "         distinct characters (besides '=') in the sequence of relators."
    print "         The optional -s specifies a smaller sized output. This program "
    print "         creates a .dot file. In order to draw the graph you should use"
    print "         the command \"neato -Tps <filename> -o <out_filename>\""
    quit()

if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        usage()

    starting_location = 1

    if '-o' in sys.argv:
        outfile_name = sys.argv[sys.argv.index('-o')+1]
        starting_location += 2
    else:
        outfile_name = 'graph1.dot'
    outfile = open(outfile_name,'w')

    if '-s' in sys.argv:
        outfile.write('digraph G {\n')
        starting_location += 1
    else:
        outfile.write('digraph G {\noverlap=scale\n')

    if starting_location > len(sys.argv) - 1:
        usage()

    rels_raw = ''.join(sys.argv[starting_location:])
    raw_chars = set(rels_raw)
    if '=' in rels_raw:
        raw_chars.remove('=')
    if ',' in rels_raw:
        raw_chars.remove(',')
    generators = list(raw_chars)
    relators = process_relators(rels_raw)

    c = cayley_graph(generators,relators,100)
    c.draw_cayley(outfile)
    outfile.write('}\n')

# EXAMPLE:
# $ python cayley_graph.py -o graph1.dot aa, bbbbb, ababab
# $ neato -Tps graph1.dot -o graph1.ps
