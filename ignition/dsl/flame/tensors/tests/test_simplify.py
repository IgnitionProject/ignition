from sympy import S

from ignition.dsl.flame.tensors import simplify, T, Tensor

def test_mul_inverse():
    delta_11 = Tensor('delta_11', 0)
    r_1, p_1 = map(lambda x: Tensor(x, 1), ['r_1', 'p_1'])
    A = Tensor('A', 2)
    a = Tensor('a', 0)

    expr = (-(T(p_1)*A*p_1)*(T(p_1)*A*r_1)*a + (T(p_1)*A*r_1))
    expr = expr.subs(a, (T(p_1)*A*p_1)**-1)
    assert(simplify(expr) == S(0))
