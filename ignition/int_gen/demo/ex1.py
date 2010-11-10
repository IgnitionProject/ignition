from sympy import *
from int_gen import *

u = DiscFunc("u")
x = Symbol("x")
cos_x = Func(cos(x), x)
sin_x = Func(sin(x), x)
dx = Dom(x, 0, 1)

integral = (cos_x*u + sin_x)*dx
gen_file("ex1", [integral],  ["eval_gen"], ['u'])
