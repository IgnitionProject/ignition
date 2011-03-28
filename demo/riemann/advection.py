from ignition.riemann import *

q = Conserved('q')
w = q.fields(['w'])
u = Constant('u')
f=[u*w]

generate("advection_kernel.py",f,q)
