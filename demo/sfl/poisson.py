from ignition.sfl.language import *
from ignition.sfl.generators import generate

u = Variable('u', dim=3, space='L2')
K = Coefficient('K', rank=1)

expr = div(K * div(u)) * dX

generate('proteus', expr)
