import sys
import fractions as fr
OUTPUT = sys.stdout

# outputs matrix in TeX format with align*
def output_tex(mat):
    OUTPUT.write('\\begin{bmatrix}\n\t\t')
    for r in range(len(mat)):
        row = mat[r]
        for c in range(len(row)):
            output_str = convert_frac(row[c])
            OUTPUT.write(output_str)
            if c < len(row) - 1:
                OUTPUT.write(' & ')
            elif r < len(mat) - 1:
                OUTPUT.write('\\\\\n\t\t')
            else:
                OUTPUT.write('\n')
    OUTPUT.write('\\end{bmatrix}\n')

# convert to string, that is
def convert_frac(frac):
    if frac.denominator == 1:
        return str(frac.numerator)
    if frac.numerator == 0:
        return "0"
    return str(frac.numerator) + '/' + str(frac.denominator)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: python mattex.py <input_file>'
        quit()
    f_name = sys.argv[1]

    with open(f_name) as f:
        to_write = []
        for line in f:
            ls = line.split()
            if len(ls) > 0:
                to_write.append(map(lambda x: fr.Fraction(x), ls))
        output_tex(to_write)
        
