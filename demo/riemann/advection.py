from ignition.riemann import *

q = Conserved('q')
(w,) = q.fields(['w'])
u = Constant('u')
f = [u * w]

g = Generator(flux=f, conserved=q)
g.eig_method = "symbolic"
g.write("advection_kernel.py")
