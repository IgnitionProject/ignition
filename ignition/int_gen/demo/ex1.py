from sympy import *
from ignition.int_gen import *

init_quad_rule(2, "Gauss")

u = DiscFunc("u")
x = Symbol("x")
cos_x = Func(cos(x), x)
sin_x = Func(sin(x), x)
dx = Dom(x, 0, 1)

integral = (cos_x * u + sin_x) * dx
gen_file("ex1", [integral], ["eval_gen"], ['u'])
