import sympy
import numpy
import scipy

from ignition.dsl.riemann.language import *

q = Conserved('q')
p, u = q.fields(['p','u'])
rho = Constant('rho')
K = Constant('K')

f = [ K*u ,
      p/rho]

A = sympy.Matrix(q.jacobian(f))
As = A.eigenvects
An = numpy.matrix([[0, 1.],[.5,0]], dtype=numpy.float32)

print A
print As
print An


evals, v1 = numpy.linalg.eig(An)
evals_2, v2 = numpy.linalg.eig(An.transpose())
#L = L.transpose()
lam = numpy.diag(evals)
L = v1
R = v2.transpose()
print "L", L
print "lambda",  lam
print "R",  R
#print "R*lambda*L", R*lam*L.transpose()
print "L*lambda*R", L*lam*R
print evals, evals_2
