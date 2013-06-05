import darcy_eqn

from ignition import sin, cos, x

myDarcy = darcy_eqn.eqn
myDarcy.u.dim = 2
myDarcy.a = 0.01 #converts RegionConstant to Constant(value=0.01)
myDarcy.f = sin(x[0])*cos(x[1]) #converts GenericField to SpatialField

coefficients = generate_coefficients('proteus', myDarcy)

#future, combine with numerics to do SFL+
#levelModel = genProteusModel(eqn = myDarcy, numerics=my_simple_gw_c0p1_n)
