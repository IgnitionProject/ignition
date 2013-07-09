from sympy import S, Symbol
from sympy.utilities.pytest import raises
from ignition.dsl.flame.tensors import (ConformityError, I, Inverse, one, T,
                                    Tensor, solve_vec_eqn)


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

def testZero():
    A = Tensor('A', 2)
    a = Tensor('a', 1)
    alpha = Tensor('alpha', 0)
    Z = Tensor('0', 2)
    z = Tensor('0', 1)
    z_0 = Tensor('0', 0)

    assert(A + Z == A)
    assert(Z + A == A)
    assert(A * Z == Z)
    assert(Z * A == Z)

    assert(a + z == a)
    assert(z + a == a)
    assert(A * z == z)
    assert(T(a) * z == z_0)
    assert(T(z) * a == z_0)
    assert(z * T(a) == Z)
    assert(a * T(z) == Z)

    assert(alpha + z_0 == alpha)
    assert(alpha * z_0 == z_0)
    assert(alpha * z == z)
    assert(alpha * Z == Z)

    assert(z_0 * A == Z)
    assert(z_0 * a == z)
    assert(A + z_0 == A)
    assert(z_0 + A == A)

    #raises(ConformityError, "z*A")
    #raises(ConformityError, "z+A")
    #raises(ConformityError, "z_0+A")


def testOne():
    A = Tensor('A', 2)
    a = Tensor('a', 1)
    alpha = Tensor('alpha', 0)
    ONE = Tensor('1', 2)
    one = Tensor('1', 0)

    assert(A * ONE == A)
    assert(ONE * A == A)

    assert(A * one == A)
    assert(one * A == A)
    assert (a * one == a)
    assert (one * a == a)
    assert(alpha * one == alpha)
    assert(one * alpha == alpha)

def testUpdate():
    k = Symbol('k')
    A = Tensor('A', 2)
    A_TL = A.update(l_ind='TL')
    A_TL_2 = A_TL.update(u_ind='2', rank=2)
    A_01 = A_TL.update(l_ind='01', shape=(k, k))
    a_02 = T(A_TL.update(l_ind='02', shape=(1, k), rank=1))

    assert(A_TL == Tensor('A_TL', 2))
    assert(A_TL_2 == Tensor('A_TL^2', 2))
    assert(A_01 == Tensor('A_01', 2, shape=(k, k)))
    assert(a_02 == T(Tensor('a_02', 1, shape=(1, k))))

def testZeroOne():
    ZERO = Tensor('0', 2)
    One = Tensor('1', 1)
    k = Tensor('k', 1)
    assert(k - ZERO * One == k)

def testInverseMul():
    ans = 5*I
    A = Tensor('A', rank=2, has_inv=True)
    A_I = Inverse(A)
    e = 5*A
    assert(A_I * e == ans)
    assert(e*A_I == ans)
    e = 5*A_I
    assert(A * e == ans)
    assert(e*A == ans)

    ans = 5*one
    p = Tensor('p', rank=1)
    pAp = T(p)*A*p
    pAp_I = Inverse(pAp)
    e = 5*pAp
    assert(e*pAp_I == ans)
    assert(pAp_I*e == ans)
    e = 5*pAp_I
    assert(e*pAp == ans)
    assert(pAp*e == ans)

    e = 5*pAp*A
    assert(A_I*e == 5*pAp*I)
    assert(e*pAp_I == 5*A)


if __name__ == "__main__":
    test_numpy_print()
