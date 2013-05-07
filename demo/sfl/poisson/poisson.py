from ignition.sfl.language import *
from ignition.sfl.generators import generate

u = Variable('u', dim=3, space='L2')
K = Coefficient('K', rank=0)

expr = div(K * grad(u))

generate('proteus', expr).to_file()
