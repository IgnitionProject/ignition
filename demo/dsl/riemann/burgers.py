from ignition.dsl.riemann import *

q = Conserved('q')
(u,) = q.fields(['u'])
f = [.5 * u ** 2]

generate(flux=f, conserved=q, filename="burgers_kernel.py")
