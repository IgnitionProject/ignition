from ignition.dsl.sfl.language import *

u = Variable('u')
b = Variable('b', rank=1)
eqn = Dt(u) + div(b*u)
