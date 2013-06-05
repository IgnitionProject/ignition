from ignition.sfl.language import *

u = Variable('u')
f = Coefficient('f')
rho, mu, g = Constants('rho mu g')
k_i = RegionConstant()
a = (k_i * rho * g) / mu
eqn = div(-a * grad(u)) - f
