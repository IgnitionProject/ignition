from ignition.dsl.flame.tensors import (numpy_print, latex_print, T, Tensor)

delta_1, omega_2, pi_1, pi_2, gamma_2, mu_12 = \
    map(lambda x: Tensor(x, rank=0),
        ['delta_1', 'omega_2', 'pi_1', 'pi_2', 'gamma_2', 'mu_12'])
r_1, r_2, q_1, q_2, p_1, p_2, s_1, s_2, x_1 = \
    map(lambda x: Tensor(x, rank=1),
        ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 's_1', 's_2', 'x_1'])
A, R_0, P_0 = map(lambda x: Tensor(x, rank=2), ['A', 'R_0', 'P_0'])

def test_numpy_print():
    assert(numpy_print(-mu_12 * p_1 + r_2) == "-dot(mu_12, p_1) + r_2")
    assert(numpy_print(delta_1 * A * p_1 + r_1) == "dot(delta_1, dot(A, p_1)) + r_1")
    assert(numpy_print(delta_1 * p_1 + x_1) == "dot(delta_1, p_1) + x_1")
    assert(numpy_print((T(r_1) * r_1) / (T(r_1) * A * p_1)) == \
                       "dot(dot((r_1).transpose(), r_1), 1.0 / (dot(dot((p_1).transpose(), A), r_1)))")
    assert(numpy_print((T(p_1) * A * r_2) / (T(p_1) * A * p_1)) == \
                       "dot(dot(dot((p_1).transpose(), A), r_2), 1.0 / (dot(dot((p_1).transpose(), A), p_1)))")

def test_latex_print():
    assert(latex_print(-mu_12 * p_1 + r_2) == "-\mu_{12} p_1 + r_2")
    assert(latex_print(delta_1 * A * p_1 + r_1) == "\delta_1 A p_1 + r_1")
    assert(latex_print(delta_1 * p_1 + x_1) == "\delta_1 p_1 + x_1")
    assert(latex_print((T(r_1) * r_1) / (T(r_1) * A * p_1)) == \
           "{r_1}^t r_1 1.0 / ({p_1}^t A r_1)")
    assert(latex_print((T(p_1) * A * r_2) / (T(p_1) * A * p_1)) == \
           "{p_1}^t A r_2 1.0 / ({p_1}^t A p_1)")
