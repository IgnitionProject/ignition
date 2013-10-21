from ignition.dsl.sfl.language import *
from ignition.utils.proteus.coefficient import sfl_coefficient

h, q = Variables('h q')
g, nu = Constants('g nu')
dbdx = Coefficients('dbdx')
u = q/h

expr1 = Dt(h) + div(q)
expr2 = Dt(q) + div(u*q + 0.5*g*h**2 - nu*grad(u)) + g*h*dbdx

strong_form = StrongForm([expr1, expr2], components=[h, q])

swe_coefficients = sfl_coefficient(strong_form)
