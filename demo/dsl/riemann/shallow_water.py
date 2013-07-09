from ignition.dsl.riemann import *

q = Conserved('q')
h, uh = q.fields(['h', 'uh'])
u = uh / h
g = Constant('g')

f = [ uh ,
      u * uh + .5 * g * h ** 2]

generate(flux=f, conserved=q, filename = "shallow_water_kernel.py")
