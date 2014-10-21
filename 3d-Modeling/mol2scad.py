import sys
from math import asin, pi
import os.path
from numpy import *

RESOLUTION = str(50)
SCALE = 10

def rad2deg(r):
    return r * 180.0 / pi

def translateSCAD(v):
    v = [str(i) for i in v]
    return 'translate([' + v[0] + ',' + v[1] + ',' + v[2] + '])'

def rotateSCAD(a,v):
    a = str(a)
    v = [str(coord) for coord in v]
    return 'rotate(a=%s, v=[%s,%s,%s])' % (a,v[0],v[1],v[2])

def sphereSCAD(r):
    return 'sphere(r=' + r + ', $fn=' + RESOLUTION + ');'

def atomSphere(v,r):
    return translateSCAD(v) + '{' + sphereSCAD(r) + '}\n'

def cylinderSCAD(r,h):
    return 'cylinder(r=' + r + ', h=' + h + ', $fn=' + str(float(RESOLUTION) / 2) + ');'

f_name = sys.argv[1]
if not f_name[len(f_name)-4:len(f_name)] == '.mol':
    sys.stderr.write('Unknown file extension. Quitting.')
    quit()

with open(f_name,'r') as f_in:
    with open(f_name[0:len(f_name)-4] + '.scad', 'w') as f_out:
        rl = f_in.readline().strip()
        f_out.write('/* ' + rl + ' */\n')
        rl = f_in.readline().strip()
        while len(rl) == 0 or not rl[0] in '1234567890': # skip past header lines
            rl = f_in.readline().strip()
        if not 'V2000' in rl:
            sys.stderr.write('Warning: ' + f_name + ' does not appear to be a V2000 .mol file.\n')
        numAtoms = int(rl[0:3])
        numBonds = int(rl[3:6])
        atoms = []
        bonds = []
        for i in range(numAtoms):
            rl = f_in.readline().strip().split()
            atoms.append([x * SCALE for x in [float(rl[0]), float(rl[1]), float(rl[2])]])
        for i in range(numBonds):
            rl = f_in.readline()
            b1 = int(rl[0:3])
            b2 = int(rl[3:6])
            b3 = int(rl[6:9])
            bonds.append([b1 - 1, b2 - 1, b3])
            # bond = [a,b,c] ==> a connects to b with c = number of bonds
            # minus 1 to account for one-vs-zero indexing
        minDist = linalg.norm(matrix(atoms[0]) - matrix(atoms[1]))
        for a1 in atoms:
            for a2 in atoms:
                if a1 == a2:
                    continue
                dist = linalg.norm(matrix(a1) - matrix(a2))
                if dist < minDist:
                    minDist = dist
        rSphere = str(minDist / 3)
        rCyl = str(minDist / 20.)
        atomsStart = set([b[0] for b in bonds]) #these atoms are the start of some bond
        atomsNoStart = set(range(len(atoms))).difference(atomsStart) # these are not.
        for i in atomsNoStart:
            f_out.write(atomSphere(atoms[i],rSphere))
        f_out.write('\n')
        for i in atomsStart:
            a = atoms[i]
            f_out.write(translateSCAD(a) + '{\n\t')
            f_out.write(sphereSCAD(rSphere) + '\n')
            for b in bonds:
                if b[0] == i:
                    v1 = a
                    v2 = atoms[b[1]]
                    v = [v2_i - v1_i for v1_i,v2_i in zip(v1,v2)]
                    ang = rad2deg(arccos(dot([0,0,1],v) / linalg.norm(v)))
                    rot = rotateSCAD(ang,cross([0,0,1],v))
                    cyl = cylinderSCAD(rCyl,str(linalg.norm(matrix(v2) - matrix(v1))))
                    if b[2] == 1 or b[2] == 4:
                        f_out.write('\t' + rot + '{\n\t\t')
                        f_out.write(cyl + '\n\t')
                        f_out.write('}\n')
                    if b[2] == 2:
                        f_out.write('\t' + rot + '{\n\t\t')
                        f_out.write(translateSCAD([-float(rSphere)/3.,0,0]) + '{\n\t\t\t')
                        f_out.write(cyl + '\n\t\t')
                        f_out.write('}\n\t\t')
                        f_out.write(translateSCAD([float(rSphere)/3.,0,0]) + '{\n\t\t\t')
                        f_out.write(cyl + '\n\t\t')
                        f_out.write('}\n\t')
                        f_out.write('}\n')
                    if b[2] == 3:
                        sqrt3over4 = 3**.5 / 4
                        f_out.write('\t' + rot + '{\n\t\t')
                        f_out.write(translateSCAD([-float(rSphere)*.4,0,-float(rSphere)*sqrt3over4*.8]) + '{\n\t\t\t')
                        f_out.write(cyl + '\n\t\t')
                        f_out.write('}\n\t\t')
                        f_out.write(translateSCAD([0,0,float(rSphere)*sqrt3over4]) + '{\n\t\t\t')
                        f_out.write(cyl + '\n\t\t')
                        f_out.write('}\n\t')
                        f_out.write(translateSCAD([.4*float(rSphere),0,-float(rSphere)*sqrt3over4*.8]) + '{\n\t\t\t')
                        f_out.write(cyl + '\n\t\t')
                        f_out.write('}\n\t')
                        f_out.write('}\n')
            f_out.write('}\n\n')


