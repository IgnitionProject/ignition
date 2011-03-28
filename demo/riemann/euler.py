from ignition.riemann import *

q = Conserved('q')
rho, rhou, E = q.fields(['rho','rhou','E'])
u = rhou/rho
gamma = Constant('gamma')
P = gamma*(E-.5*u*rhou)

f = [rhou,
     P+u*rhou,
     u*(E+p)]

generate("euler_kernel.py",f,q)
