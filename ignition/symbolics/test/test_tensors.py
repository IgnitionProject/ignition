from sympy import S
from ignition.symbolics.tensors import numpy_print, T, Tensor, solve_vec_eqn

delta_1, omega_2, pi_1, pi_2, gamma_2, mu_12 = \
    map(lambda x: Tensor(x, rank=0),
        ['delta_1', 'omega_2', 'pi_1', 'pi_2', 'gamma_2', 'mu_12'])
r_1, r_2, q_1, q_2, p_1, p_2, s_1, s_2, x_1 = \
    map(lambda x: Tensor(x, rank=1),
        ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 's_1', 's_2', 'x_1'])
A, R_0, P_0 = map(lambda x: Tensor(x, rank=2), ['A', 'R_0', 'P_0'])


def test_algebra():
    eqn = -2 * (T(p_1) * A * r_2) / (T(p_1) * A * p_1) * (T(p_1) * A * r_2)
    eqn -= -2 * (T(p_1) * A * r_2) * (T(p_1) * A * r_2) / (T(p_1) * A * p_1)
    assert(eqn == S(0))
    assert(T(p_1) * A * r_2 == T(r_2) * A * p_1)

def test_vec_solve():
    mu_12 = Tensor('mu_12', rank=0)
    p_1, p_2 = map(lambda x: Tensor(x, rank=1), ['p_1', 'p_2'])
    A = Tensor('A', rank=2)
    print solve_vec_eqn(-mu_12 * (T(p_1) * A * p_2) - mu_12 * (T(p_2) * A * p_1) + (T(p_2) * A * p_1) , mu_12)

def test_numpy_print():
    assert(numpy_print(-mu_12 * p_1 + r_2) == "-dot(mu_12, p_1) + r_2")
    assert(numpy_print(delta_1 * A * p_1 + r_1) == "dot(delta_1, dot(A, p_1)) + r_1")
    assert(numpy_print(delta_1 * p_1 + x_1) == "dot(delta_1, p_1) + x_1")
    print numpy_print((T(r_1) * r_1) / (T(r_1) * A * p_1))
    #dot(dot(r_1, r_1), (1.0/dot(transpose(dot(transpose(p_1), A)), r_1)))
    print numpy_print((T(p_1) * A * r_2) / (T(p_1) * A * p_1))
    #dot(dot(transpose(dot(transpose(p_1), A)), r_2), (1.0/dot(transpose(dot(transpose(p_1), A)), p_1)))

if __name__ == "__main__":
    test_numpy_print()
