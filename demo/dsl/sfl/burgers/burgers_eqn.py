from ignition.sfl.language import *

u = Variable('u')
f = u**2
eqn = Dt(u) + div(f)
