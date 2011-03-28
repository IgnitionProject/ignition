from ignition.riemann import *

q = Conserved('q')
u = q.fields(['u'])
f=[.5*u**2]

generate("burgers_kernel.py",f,q)
