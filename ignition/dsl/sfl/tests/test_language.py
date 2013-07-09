from ignition.dsl.sfl.language import (Coefficients, Constant, Constants, grad, Dt, div, StrongForm, Variable, Variables)


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
    strong_form = StrongForm(c*grad(div(u)) + div(v) - f)

    order_dict = strong_form.separate_by_order()
    print order_dict
    assert(order_dict[0] == -f)
    assert(order_dict[1] == div(v))
    assert(order_dict[2] == c*grad(div(u)))


def test_extract_transport_coefficients():
    u = Variable('u')
    
    a, b, c, d = Coefficients('a b c d')
    eqn = Dt(a*u) + div(b*u + c*grad(u)) + d*u
    strong_form = StrongForm(eqn)

    print strong_form.extract_transport_coefficients()
    assert(False)

test_extract_transport_coefficients()
