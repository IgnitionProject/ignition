from ignition.dsl.sfl.language import (Coefficients, Constant, Constants, grad, Dt, dot, div, StrongForm, Variable, Variables)


def test_StrongForm():
    a, b = Variables('a b')
    c = Constant('c')
    strong_form = StrongForm(c*a*b)
    assert(strong_form.a is a)

    strong_form.a.dim = 1
    strong_form.b.dim = 1
    assert(a.dim == 1)
    assert(b.dim == 1)

    strong_form.c = 1.0
    assert(c.val == 1.0)


def test_variables():
    u = Variable('u')
    c = Constant('c')
    strong_form = StrongForm(c*u)

    assert(strong_form.variables() == set([u]))


def test_separate_by_order():
    u, v = Variables('u v')
    c, f = Constants('c f')
    strong_form = StrongForm(c*grad(div(u)) + div(v) - f + dot(c, grad(u)))

    order_dict = strong_form.separate_by_order()
    assert(order_dict[0] == -f)
    assert(order_dict[1] == div(v) + dot(c, grad(u)))
    assert(order_dict[2] == c*grad(div(u)))


def test_extract_transport_coefficients():
    u = Variable('u', rank=0)
    a, b, d = Coefficients('a b d', rank=0)
    b, e = Coefficients('b e', rank=1)
    c, = Coefficients('c', rank=2)

    eqn = Dt(a*u) + div(b*u + c*grad(u)) + d*u + dot(e, grad(u))
    strong_form = StrongForm(eqn)

    coeffs = {'diffusion': c,
              'reaction': d*u,
              'hamiltonian': dot(e, grad(u)),
              'potential': u,
              'mass': Dt(a*u),
              'advection': b*u,
              }
    sf_coeffs = strong_form.extract_transport_coefficients()
    assert(coeffs == sf_coeffs)
    eqn =  d*u + dot(e,grad(u)) + Dt(a*u) + div(b*u) + div(c*grad(u))
    sf_coeffs = strong_form.extract_transport_coefficients()
    assert(coeffs == sf_coeffs)


def test_create_order_dictionary():
    u = Variable('u', rank=0)
    a, b, d = Coefficients('a b d', rank=0)
    b, e = Coefficients('b e', rank=1)
    c, = Coefficients('c', rank=2)

    eqn = Dt(a*u) + div(b*u + c*grad(u)) + d*u + e*grad(u)
    strong_form = StrongForm(eqn)

    tc_dict = {'mass': {0: 'linear'},
               'advection': {0: 'linear'},
               'diffusion': {0: 'constant'},
               'potential': {0: 'linear'},
               'reaction': {0: 'linear'},
               'hamiltonian': {0: 'linear'},
               }
    computed_tc_dict = strong_form.transport_coefficient_dictionary(u)
    assert(tc_dict == computed_tc_dict)
