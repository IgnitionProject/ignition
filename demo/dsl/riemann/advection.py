from sympy import Matrix

from ignition.dsl.riemann import *

q = Conserved('q')
(w,) = q.fields(['w'])
u = Constant('u')
f = [u * w]

g = Generator(flux=f, conserved=q)
g.eig_method = "symbolic"
g.write("advection_kernel.py")

c = ConstantField('c')
A = Matrix([[c*u]])
generate(A=A, conserved=q, constant_fields=[c],
         filename="variable_advection_kernel.py")

generate(A=A, conserved=q, constant_fields=[c], evaluation="vectorized",
         filename="variable_advection_vectorized_kernel.py")

generate(A=A, conserved=q, constant_fields=[c], evaluation="vectorized",
         eig_method="numerical",
         filename="variable_advection_numerical_vectorized_kernel.py")
