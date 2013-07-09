from ignition.dsl.riemann import *

q = Conserved('q')
rho, rhou, E = q.fields(['rho', 'rhou', 'E'])
u = rhou / rho
gamma = Constant('gamma')
P = gamma * (E - .5 * u * rhou)

f = [rhou,
     P + u * rhou,
     u * (E + P)]

#generate(f, q, "euler_kernel.py")
G = Generator()
G.flux = f
G.conserved = q
G.eig_method = "numerical"
G.write("euler_kernel.py")
