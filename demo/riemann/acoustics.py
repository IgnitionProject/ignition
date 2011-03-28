from ignition.riemann import *

q = Conserved('q')
p, u = q.fields(['p','u'])
rho = Constant('rho')
K = Constant('K')

f = [ K*u ,
      p/rho]

generate("acoustics_kernel.py",f,q)
