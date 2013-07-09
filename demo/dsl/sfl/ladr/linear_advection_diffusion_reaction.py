from ignition.dsl.sfl.language import *
from ignition.dsl.sfl.generators import generate

u = Variable('u', dim=3, space='L2')
M = Coefficient('M', rank=1, dim=3)
A = Coefficient('A', rank=1, dim=3)
B = Constant('B', [1.0, 1.0, 1.0])
C = Coefficient('C', rank=1, dim=3)

expr = M * Dt(u) + div(B*u - A*grad(u)) + C*u
generate('proteus', expr)
