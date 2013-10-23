from ignition.dsl.sfl.language import *
from ignition.dsl.sfl.generators import ProteusCoefficientGenerator


def test_proteus_coefficient_create_order_dictionary():
    u = Variable('u', rank=0)
    a, b, d = Coefficients('a b d', rank=0)
    b, e = Coefficients('b e', rank=1)
    c, = Coefficients('c', rank=2)

    eqn = Dt(a*u) + div(b*u + c*grad(u)) + d*u + e*grad(u)
    strong_form = StrongForm(eqn)
    coeff_gen = ProteusCoefficientGenerator(strong_form)

    tc_dict = {'mass': {0: {0: 'linear'}},
               'advection': {0: {0: 'linear'}},
               'diffusion': {0: {0: 'constant'}},
               'potential': {0: {0: 'linear'}},
               'reaction': {0: {0: 'linear'}},
               'hamiltonian': {0: {0: 'linear'}},
               }
    computed_tc_dict = coeff_gen.gen_transport_coefficient_dictionary()
    assert(tc_dict == computed_tc_dict)
