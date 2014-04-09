# http://en.wikipedia.org/wiki/Knuth%E2%80%93Bendix_completion_algorithm
import sys

class knuth_bendix:
    def __init__(self,relators,MAX_DEPTH):
        self.MAX_DEPTH = MAX_DEPTH
        self.reductions = set()
        for rel in relators:
            p = rel[0]*rel[1]
            q = rel[2]*rel[3]
            self.add_red(p,q)
        self.update_reds()
        self.expand_reds()

    # add the reduction p -> q in sorted order (q < p)
    def add_red(self,p,q):
        if p == q:
            return
        assert(p != '')
        if len(q) < len(p) or (len(q) == len(p) and q < p):
            self.reductions.add((p,q))
        else:
            self.reductions.add((q,p))

    # reduce the word "a" using ONLY given reduction "red"
    def reduce_given(self,a,red):
        # first, guarantee termination.
        assert(red[0] != red[1])
        assert(red[0] != '')
        assert(red[0] not in red[1])
        while red[0] in a:
            idx = a.index(red[0])
            a = a[:idx] + red[1] + a[idx + len(red[0]):]
        return a

    # reduce the word "a" using all known rules, EXCEPT itself
    def reduce_almost_all(self,a):
        for red in self.reductions:
            if red[0] == a:
                continue
            a = self.reduce_given(a,red)
        return a

    # reduce the word "a" using all known rules
    def reduce_all(self,a):
        changes_made = True
        while changes_made:
            changes_made = False
            for red in self.reductions:
                change = self.reduce_given(a,red)
                if a != change:
                    changes_made = True
                    a = change
        return a

    # for outside world's use
    def simplify(self,a):
        return self.reduce_all(a)

    # replaces all current reductions with any other reductions possible.
    def update_reds(self):
        changes_made = True
        while changes_made:
            changes_made = False
            reductions_copy = self.reductions.copy()
            for red in reductions_copy:
                red1_reduced = self.reduce_all(red[1])
                red0_reduced = self.reduce_almost_all(red[0])
                if red1_reduced != red[1] or red0_reduced != red[0]:
                    changes_made = True
                self.reductions.remove(red)
                self.add_red(red0_reduced,red1_reduced)

    def expand_reds(self):
        have_checked = {}
        self.more_to_check = True
        self.iters = 0
        while self.more_to_check:
            self.more_to_check = False
            self.iters += 1
            if self.iters > self.MAX_DEPTH:
                sys.stderr.write('Reached maximum iteration depth, quitting\n')
                quit()
            reductions_copy = self.reductions.copy()
            for red_1 in reductions_copy:
                for red_2 in reductions_copy:
                    if (red_1,red_2) in have_checked or red_1 == red_2:
                        continue
                    have_checked[(red_1,red_2)] = True
                    p1 = red_1[0]
                    q1 = red_1[1]
                    p2 = red_2[0]
                    q2 = red_2[1]
                    does_overlap = self.overlap(p1,p2)
                    A,B,C = None,None,None
                    if does_overlap:
                        (A,B,C) = does_overlap
                    elif p2 in p1:
                        idx = p1.index(p2)
                        (A,B,C) = (p1[:idx], p2, p1[idx:])
                    if A:
                        ABC = A + B + C
                        r1 = self.reduce_given(ABC,(p1,q1))
                        r2 = self.reduce_given(ABC,(p2,q2))
                        self.add_red(r1,r2)
                        self.more_to_check = True
            self.update_reds()

    def overlap(self,a,b):
        for i in range(len(b))[::-1]:
            if a[-i:] == b[:i]:
                return (a[:-i], b[:i], b[i:])
        return False

    def show_reds(self):
        max_len = 0
        for red in self.reductions:
            max_len = max(len(red[0]),max_len)
        for red in self.reductions:
            print ('"' + red[0] + '" ' + '-'*(max_len - len(red[0]) + 1)
             + '-> ' + '"' + red[1] + '"')

