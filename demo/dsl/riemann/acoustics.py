from ignition.dsl.riemann import *

q = Conserved('q')
p, u = q.fields(['p','u'])
rho = Constant('rho')
K = Constant('bulk')

f = [ K*u ,
      p/rho]

#generate(f, q, "acoustics_kernel.py")

G = Generator(flux=f, conserved=q)
G.eig_method="symbolic"
G.write("acoustics_kernel.py")

import sympy as sp

A = sp.Matrix([[0, K],[1.0/rho, 0]])
generate(A=A, conserved=q, filename="acoustics_kernel_from_A.py")

generate(flux=f, conserved=q, evaluation="vectorized", filename="acoustics_kernel_vectorized.py")

G = Generator(flux=f, conserved=q)
G.eig_method = "numerical"
G.evaluation = "vectorized"
G.write("acoustics_kernel_vectorized_numerical.py")

