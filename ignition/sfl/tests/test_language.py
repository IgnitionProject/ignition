from ignition.sfl.language import Constant, StrongForm, Variables


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
