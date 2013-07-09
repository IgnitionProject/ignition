from ignition.dsl.sfl.language import *

from sympy import latex

u = Variable('u')
f = Coefficient('f')
rho, mu, g = Constants('rho mu g')
k_i = RegionConstant('k_i')
a = (k_i * rho * g) / mu
eqn = strong_form(div(-a * grad(u)) - f)

print "eqn:", latex(eqn)
