# platonic.py
# run "python platonic.py help" for help/instructions on running the program.

from math import sin, cos, asin, acos, pi
from numpy import *
import itertools
import sys
from sys import argv
import os.path

class platonic:
    def __init__(self,name,scale=1):
        self.name = name.lower() # keep name
        self.scale = scale # keep scale
        self.zero = [[0],[0],[0],[1]] # extending to fourth dimension
                                      # so translations can be matrices
        self.s = self.schlafli(name) # schlafli symbol
        if not self.s:
            sys.stderr.write('Unknown name of platonic solid. Quitting.')
            quit()

        self.dRot = self.dihedralAngleRot() # dihedral rotation matrices
        self.fRot = self.faceAngleRot() # face rotation matrix
        self.eps = 1e-5 # epsilon for float comparisons
        self.ft = self.face_transforms() # array of matrices

        self.fcs = self.faces([],identity(4),0) # set of faces
        ret = self.ptsAndFaces() # open SCAD model is left unscaled
        self.pts = ret[0]
        self.SCADfcs = ret[1]
        self.fcs = [[scale * pt for pt in face] for face in self.fcs] # scaling
            
    # returns schlafli symbol
    def schlafli(self,name):
        if name.lower() == "tetrahedron":
            return [3,3]
        elif name.lower() == "cube":
            return [4,3]
        elif name.lower() == "octahedron":
            return [3,4]
        elif name.lower() == "dodecahedron":
            return [5,3]
        elif name.lower() == "icosahedron":
            return [3,5]
        else:
            return False

    # returns rotation matrix around x-axis of dihedral angle,
    # the first is in positive direction, second in negative
    def dihedralAngleRot(self):
        ang = 2 * asin( cos(pi / self.s[1]) / sin(pi / self.s[0]) )
        return [matrix([[1,0,0,0],
                        [0,cos(ang),-sin(ang),0],
                        [0,sin(ang),cos(ang),0],
                        [0,0,0,1]]),
                matrix([[1,0,0,0],
                        [0,cos(ang),sin(ang),0],
                        [0,-sin(ang),cos(ang),0],
                        [0,0,0,1]])]

    # returns rotation matrix of EXTERIOR angle of face around z-axis
    def faceAngleRot(self):
        ang = (2 * pi) / self.s[0]
        return matrix([[cos(ang), -sin(ang), 0, 0],
                       [sin(ang), cos(ang), 0, 0],
                       [0,0,1,0],
                       [0,0,0,1]])

    # [T * self.zero for T in ft] is the set of points on each face
    def face_transforms(self):
        verts = self.s[0] # number of vertices on face
        translation = matrix([[1,0,0,1],
                              [0,1,0,0],
                              [0,0,1,0],
                              [0,0,0,1]])
        ft = [linalg.matrix_power(translation * self.fRot,i) for i in range(verts)]
        return ft

    def isInPts(self,curr_pts,curr_pt):
        for pt in curr_pts:
            if linalg.norm(pt-curr_pt) < self.eps:
                return True
        return False

    def isInFaces(self,curr_faces,triangle):
        for face in curr_faces:
            if all([self.isInPts(face,pt) for pt in triangle]):
                return True
        return False

    # used to generate STL format
    def faces(self,curr_fcs,curr_trans,parity):
        pts = [curr_trans * T * self.zero for T in self.ft]
        if parity:
            face = [[pts[0],pts[i],pts[i+1]] for i in range(1,len(pts)-1)]
        else:
            face = [[pts[0],pts[i+1],pts[i]] for i in range(1,len(pts)-1)]
        # this next line checks if any triangle in the current face shares
        # the same points as a previously defined triangle. If this is the
        # case, then we can assume the whole face has already been covered
        if not any([self.isInFaces(curr_fcs,c) for c in itertools.combinations(pts,3)]):
            curr_fcs = curr_fcs + face
            for T in self.ft:
                curr_fcs = self.faces(curr_fcs,curr_trans * T * self.dRot[parity], (parity + 1) % 2)
        return curr_fcs

    # used to generate openSCAD format
    def ptsAndFaces(self):
        pts = []
        for face in self.fcs:
            for pt in face:
                if not self.isInPts(pts,pt):
                    pts.append(pt)
        faces = []
        for face in self.fcs:
            SCADface = []
            for vert in face:
                for i in range(len(pts)):
                    pt = pts[i]
                    if self.isInPts([pt],vert):
                        SCADface.append(i)
            faces.append(SCADface)
        return [pts,faces]

    def displayOpenSCAD(self):
        out = '/* %s */\n' % self.name
        out = out + 'polyhedron(points=['
        for pt in self.pts:
            out = out + '[%.3f,%.3f,%.3f], ' % (pt[0],pt[1],pt[2])
        out = out[0:len(out)] # cutoff trailing comma
        out = out + '],\nfaces=['
        for face in self.SCADfcs:
            out = out + '[%d,%d,%d], ' % (face[0],face[1],face[2])
        out = out[0:len(out)] # cutoff trailing comma
        out = out + ']);\n'
        return out

    # returns the lower integer n such that 10^n <= x
    def power10(self,x):
        return math.floor(math.log(abs(x),10))

    def stlNum(self,x1,x2,x3):
        if abs(x1) < self.eps:
            ret1 = '0.0e+0'
        else:
            ret1 =  '%.5fe%d' % (x1 / 10**(self.power10(x1)), self.power10(x1))
        if abs(x2) < self.eps:
            ret2 = ' 0.0e+0'
        else:
            ret2 = ' %.5fe%d' % (x2 / 10**(self.power10(x2)), self.power10(x2))
        if abs(x3) < self.eps:
            ret3 = ' 0.0e+0'
        else:
            ret3 = ' %.5fe%d' % (x3 / 10**(self.power10(x3)), self.power10(x3))
        return ret1 + ret2 + ret3

    def displaySTL(self):
        tab = '    '
        tab2 = tab + tab
        out = 'solid ' + self.name + '\n'
        for f in self.fcs:
            normal = cross([float(f[0][0] - f[2][0]),float(f[0][1] - f[2][1]),float(f[0][2] - f[2][2])],
                           [float(f[1][0] - f[2][0]),float(f[1][1] - f[2][1]),float(f[1][2] - f[2][2])])
            normal = normal / linalg.norm(normal)
            out = out + 'facet normal ' + self.stlNum(normal[0],normal[1],normal[2]) + '\n'
            out = out + tab + 'outer loop\n'
            out = out + tab2 + 'vertex ' + self.stlNum(f[0][0],f[0][1],f[0][2]) + '\n'
            out = out + tab2 + 'vertex ' + self.stlNum(f[1][0],f[1][1],f[1][2]) + '\n'
            out = out + tab2 + 'vertex ' + self.stlNum(f[2][0],f[2][1],f[2][2]) + '\n'
            out = out + tab + 'endloop\n'
            out = out + 'endfacet\n'
        out = out + 'endsolid ' + self.name + '\n'
        return out

help_msg = '''This program can be run in two ways. It can be run with no command
line arguments, and you will be prompted for the platonic solid name
and scale. Alternatively, the name and scale can be passed as 
command line arguments, with the name first and scale second.

'''

# PROCESS INPUTS
if len(argv) == 1:
    name = raw_input('Name of platonic solid: ')
    scale = raw_input('Scaling factor (10 is smallish): ')
else:
    name = argv[1]
    if name in ['help', '?']:
        sys.stderr.write(help_msg)
        quit()
    if len(argv) > 2:
        scale = float(argv[2])
    else:
        scale = 1

# CREATE OUTPUT FILES
s = platonic(name,float(scale))
if os.path.isfile(name + '.stl') or os.path.isfile(name + '.scad'):
    overwrite = raw_input('This file-name already exists. Overwrite? (Y/N): ')
    if not overwrite.lower() == 'y':
        quit()
with open(name + '.stl','w') as stl:
    stl.write(s.displaySTL())
with open(name + '.scad','w') as scad:
    scad.write(s.displayOpenSCAD())


