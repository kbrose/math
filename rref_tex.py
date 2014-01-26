import sys
import fractions as fr
INIT = 0
SUBSEQUENT = 1
def rref(mat):
    curr_row = 0
    max_row = len(mat)
    curr_col = 0
    max_col = len(mat)+1 # leave out last column
    while curr_row != max_row:
        found_one = False
        for j in range(curr_col,max_col):
            for i in range(curr_row,max_row):
                if mat[i][j] != 0:
                    found_one = True
                    temp = mat[i]
                    mat[i] = mat[curr_row]
                    mat[curr_row] = temp
                    if(curr_row != i):
                        output_tex(mat,SUBSEQUENT)
                    curr_val = mat[curr_row][j]
                    mat[curr_row] = [k / curr_val for k in mat[curr_row]]
                    if curr_val != 1:
                        output_tex(mat,SUBSEQUENT)
                    for i2 in range(max_row):
                        if i2 == curr_row:
                            continue
                        to_remove = mat[i2][j]
                        if to_remove != 0:
                            mat[i2] = [mat[i2][k] - mat[curr_row][k]*to_remove for k in range(len(mat[i2]))]
                            output_tex(mat,SUBSEQUENT)
                    break
            if found_one:
                break
        curr_row += 1
        curr_col += 1
    return mat

def output_tex(mat,where_to_put):
    if where_to_put == INIT:
        sys.stdout.write('\t\\begin{align*}\n\t\\begin{bmatrix}\n\t\t')
    else:
        sys.stdout.write('\t &= \\begin{bmatrix}\n\t\t')
    for r in range(len(mat)):
        row = mat[r]
        for c in range(len(row)):
            output_str = convert_frac(row[c])
            sys.stdout.write(output_str)
            if c < len(row) - 1:
                sys.stdout.write(' & ')
            elif r < len(mat) - 1:
                sys.stdout.write('\\\\\n\t\t')
            else:
                sys.stdout.write('\n\t')
    sys.stdout.write('\\end{bmatrix}')
    if where_to_put == SUBSEQUENT:
        sys.stdout.write('\\\\\n')

def convert_frac(frac):
    if frac.denominator == 1:
        return str(frac.numerator)
    if frac.numerator == 0:
        return "0"
    return str(frac.numerator) + '/' + str(frac.denominator)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: python rref_tex.py <input_file>'
        quit()
    f_name = sys.argv[1]

    with open(f_name) as f:
        to_solve = []
        for line in f:
            ls = line.split()
            if len(ls) > 0:
                to_solve.append(map(lambda x: fr.Fraction(x), ls))
        output_tex(to_solve,INIT)
        rref_mat = rref(to_solve)
        output_tex(rref_mat,SUBSEQUENT)
        sys.stdout.write('\t\\end{align*}')

