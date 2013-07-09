from sympy import S

from ignition.dsl.flame.tensors import (expr_rank, expr_shape, solve_vec_eqn,
                                    T, Tensor, Transpose)
from ignition.dsl.flame.tensors.solvers import (all_back_sub, assump_solve,
    backward_sub, branching_assump_solve, forward_solve, sol_without_recomputes)

def test_backward_sub():
    q, r, s = map(lambda x: Tensor(x, rank=1), 'qrs')
    s_t = Transpose(s)
    delta = Tensor('delta', rank=0)
    eqn1 = r - s - q * delta
    eqn2 = s_t * r
    sol_dict, failed_var = backward_sub([eqn1, eqn2], [q, s], [r, delta])

    print sol_dict, failed_var

    sol_dict, failed_var = backward_sub([eqn1, eqn2], [q, s], [delta, r])
    print sol_dict, failed_var


def test_forward_solve():
    q, r, s = map(lambda x: Tensor(x, rank=1), 'qrs')
    delta = Tensor('delta', rank=0)
    eqn1 = s + q
    eqn2 = delta * r - q
    sol_dict = forward_solve([eqn1, eqn2], [delta, r])
    print "sol_dict should be: {q: delta*r, s: -q }"
    print "  actual:", sol_dict


def test_vec_solve():
    mu_12 = Tensor('mu_12', rank=0)
    p_1, p_2 = map(lambda x: Tensor(x, rank=1), ['p_1', 'p_2'])
    A = Tensor('A', rank=2)
    print solve_vec_eqn(-mu_12 * (T(p_1) * A * p_2) - mu_12 * (T(p_2) * A * p_1) + (T(p_2) * A * p_1) , mu_12)


def test_algebra():
    delta_1, omega_2, pi_1, pi_2, gamma_2, mu_12 = \
        map(lambda x: Tensor(x, rank=0),
            ['delta_1', 'omega_2', 'pi_1', 'pi_2', 'gamma_2', 'mu_12'])
    r_1, r_2, q_1, q_2, p_1, p_2, s_1, s_2 = \
        map(lambda x: Tensor(x, rank=1),
            ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 's_1', 's_2'])
    A, R_0, P_0 = map(lambda x: Tensor(x, rank=2), ['A', 'R_0', 'P_0'])

    eqn = -2 * (T(p_1) * A * r_2) / (T(p_1) * A * p_1) * (T(p_1) * A * r_2)
    eqn -= -2 * (T(p_1) * A * r_2) * (T(p_1) * A * r_2) / (T(p_1) * A * p_1)
    assert(eqn == S(0))

    assert(T(p_1) * A * r_2 == T(r_2) * A * p_1)

def test_0 ():
    A = Tensor('A', rank=2, has_inv=True)
    x = Tensor('x', rank=1)
    y = Tensor('y', rank=1)
    alpha = Tensor('alpha', rank=0)
    beta = Tensor('beta', rank=0)
    eqn = alpha * A * x + beta * y
    print eqn, "rank:", expr_rank(eqn)
    print "solution for y", solve_vec_eqn(eqn, y)
    print "solution for x", solve_vec_eqn(eqn, x)

# FIXME: SKIP
#def test_1 ():
#    # r = s - q * delta,  and
#    # s^t r = 0
#    #
#    # {q and s known}
#    # delta = (s^t q)^{-1} s^t s
#    # {q, s, and delta known}
#    # r = s - q*delta
#    # {all known and r = s - q * delta = 0  and s^t r = 0}
#
#    q, r, s = map(lambda x: Tensor(x, rank=1), 'qrs')
#    s_t = Transpose(s)
#    delta = Tensor('delta', rank=0)
#    eqn1 = r - s - q * delta
#    eqn2 = s_t * r
#
#    sol_r = solve_vec_eqn(eqn1, r)
#    tmp = eqn2.subs(r, sol_r).expand()
#    sol_delta = solve_vec_eqn(tmp, delta)
#    print "sol_delta:", sol_delta
#    print "sol_r:", sol_r

def test_2 ():
    from sympy import expand, S
    A = Tensor('A', rank=2)
    A_t = Transpose(A)
    B = Tensor('B', rank=2)
    x = Tensor('x', rank=1)
    y = Tensor('y', rank=1)
    x_t = Transpose(x)
    y_t = Transpose(y)
    alpha = Tensor('alpha', rank=0)
    beta = Tensor('beta', rank=0)
    teqn = Transpose((A + B) * x)
    print "teqn.expand: ", teqn.expand(), "should be x'*A' + x'*B'"

    print expand(S(2) * beta * (alpha * A + beta * B) * x), "should be 2*beta**2*B*x + 2*alpha*beta*A*x"
    print expr_shape(expand(S(2) * A * x)), "should be (n, 1)"


def test_3 ():
    q, r, s = map(lambda x: Tensor(x, rank=1), 'qrs')
    s_t = Transpose(s)
    delta = Tensor('delta', rank=0)
    eqn1 = r - s - q * delta
    eqn2 = s_t * r

    print forward_solve([eqn1, eqn2], [r, s, q])
    print forward_solve([eqn1, eqn2], [delta, s, q])
    print forward_solve([eqn2, eqn1], [delta, s, q])

def test_4 ():
    q, r, s = map(lambda x: Tensor(x, rank=1), 'qrs')
    s_t = Transpose(s)
    delta = Tensor('delta', rank=0)
    eqn1 = r - s - q * delta
    eqn2 = s_t * r

    print assump_solve([eqn1, eqn2], [s, q])

def get_chronos_eqns_1 ():
    delta_1, omega_2, pi_1, pi_2, gamma_2, mu_12 = \
        map(lambda x: Tensor(x, rank=0),
            ['delta_1', 'omega_2', 'pi_1', 'pi_2', 'gamma_2', 'mu_12'])
    r_1, r_2, q_1, q_2, p_1, p_2, s_1, s_2 = \
        map(lambda x: Tensor(x, rank=1),
            ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 's_1', 's_2'])
    A, R_0, P_0 = map(lambda x: Tensor(x, rank=2), ['A', 'R_0', 'P_0'])

    eqns = [r_2 - r_1 - delta_1 * q_1,
            q_2 - A * p_2,
            p_2 - r_2 + p_1 * mu_12,
            q_2 - A * r_2 + q_1 * mu_12,
            omega_2 - T(r_2) * r_2,
            pi_2 - T(p_2) * A * p_2,
            T(R_0) * r_2,
            T(r_1) * r_2,
            T(P_0) * A * p_2,
            T(p_1) * A * p_2,
            T(p_2) * A * p_2 - T(r_2) * A * r_2 + T(mu_12) * T(p_1) * A * p_1 * mu_12,
            ]
    knowns = [p_1, r_1, q_1, pi_1, A, R_0, P_0]
    return eqns, knowns

def get_chronos_eqns_2 ():
    delta_1, omega_2, pi_1, pi_2, gamma_2, mu_12 = \
        map(lambda x: Tensor(x, rank=0),
            ['delta_1', 'omega_2', 'pi_1', 'pi_2', 'gamma_2', 'mu_12'])
    r_1, r_2, q_1, q_2, p_1, p_2, s_1, s_2 = \
        map(lambda x: Tensor(x, rank=1),
            ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 's_1', 's_2'])
    A, R_0, P_0 = map(lambda x: Tensor(x, rank=2), ['A', 'R_0', 'P_0'])

    eqns = [r_2 - r_1 - delta_1 * q_1,
            q_2 - A * p_2,
            p_2 - r_2 + p_1 * mu_12,
            q_2 - A * r_2 + q_1 * mu_12,
            omega_2 - T(r_2) * r_2,
            pi_2 - T(p_2) * A * p_2,
            T(R_0) * r_2,
            T(r_1) * r_2,
            T(P_0) * A * p_2,
            T(p_1) * A * p_2,
            pi_2 - T(r_2) * A * r_2 + T(mu_12) * pi_1 * mu_12,
            ]
    knowns = [p_1, r_1, q_1, pi_1, A, R_0, P_0]
    return eqns, knowns

def get_chronos_eqns_3 ():
    delta_1, omega_2, pi_1, pi_2, gamma_2, mu_12 = \
        map(lambda x: Tensor(x, rank=0),
            ['delta_1', 'omega_2', 'pi_1', 'pi_2', 'gamma_2', 'mu_12'])
    r_1, r_2, q_1, q_2, p_1, p_2, s_1, s_2 = \
        map(lambda x: Tensor(x, rank=1),
            ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 's_1', 's_2'])
    A, R_0, P_0 = map(lambda x: Tensor(x, rank=2), ['A', 'R_0', 'P_0'])

    eqns = [r_2 - r_1 - delta_1 * q_1,
            q_2 - A * p_2,
            p_2 - r_2 + p_1 * mu_12,
            q_2 - A * r_2 + q_1 * mu_12,
            omega_2 - T(r_2) * r_2,
            pi_2 - T(p_2) * A * p_2,
            pi_2 - T(r_2) * A * r_2 + T(mu_12) * pi_1 * mu_12,
            T(R_0) * r_2,
            T(r_1) * r_2,
            T(P_0) * A * p_2,
            T(p_1) * A * p_2,
            ]
    knowns = [p_1, r_1, q_1, pi_1, A, R_0, P_0]
    return eqns, knowns

#def test_chronos_1(levels= -1):
#    eqns, knowns = get_chronos_eqns_1()
#    return branching_assump_solve(eqns, knowns, levels)

#def test_chronos_2(levels= -1):
#    eqns, knowns = get_chronos_eqns_2()
#    return branching_assump_solve(eqns, knowns, levels)

#def test_chronos_3(levels= -1):
#    eqns, knowns = get_chronos_eqns_3()
#    return branching_assump_solve(eqns, knowns, levels)

# FIXME: SKIP
#def test_chronos_4(levels=2, multiple_sols=False, sub_all=True):
#    eqns, knowns = get_chronos_eqns_1()
#    sols = all_back_sub(eqns, knowns, levels, multiple_sols, sub_all)
#    uniqs = {}
#    for k in sols[0][0]:
#        uniqs[k] = set(map(lambda x: x[0][k], sols))
#    print "Unique solutions for each unknown:"
#    for k in uniqs:
#        print " %s: %d" % (k, len(uniqs[k]))
#    return sols, uniqs

def test_overdetermined_back_sub():
    pi_1, pi_2, mu_12 = \
        map(lambda x: Tensor(x, rank=0),
            ['pi_1', 'pi_2', 'mu_12'])
    r_2, p_1, p_2 = \
        map(lambda x: Tensor(x, rank=1),
            ['r_2', 'p_1', 'p_2'])
    A = Tensor('A', rank=2)

    eqns = [ pi_2 - T(r_2) * A * r_2 + T(mu_12) * pi_1 * mu_12,
             p_2 - r_2 + p_1 * mu_12,
             pi_2 - T(p_2) * A * p_2,
            ]
    return backward_sub(eqns, [r_2, p_1, mu_12, A, pi_1], multiple_sols=True)

def test_overdetermined_forward_solve():
    pi_1, pi_2, mu_12 = \
        map(lambda x: Tensor(x, rank=0),
            ['pi_1', 'pi_2', 'mu_12'])
    r_2, p_1, p_2 = \
        map(lambda x: Tensor(x, rank=1),
            ['r_2', 'p_1', 'p_2'])
    A = Tensor('A', rank=2)

    eqns = [ pi_2 - T(r_2) * A * r_2 + T(mu_12) * pi_1 * mu_12,
             p_2 - r_2 + p_1 * mu_12,
             pi_2 - T(p_2) * A * p_2,
            ]
    return forward_solve(eqns, [r_2, p_1, mu_12, A, pi_1], True)

def test_5 ():
    q, r, s = map(lambda x: Tensor(x, rank=1), 'qrs')
    s_t = Transpose(s)
    delta = Tensor('delta', rank=0)
    eqn1 = r - s - q * delta
    eqn2 = s_t * r

    print assump_solve([eqn1, eqn2], [r, q])

def test_numerator ():
    a, b, c = map(lambda x: Tensor(x, rank=0), 'abc')
    expr = (a + b) / c
    sol = solve_vec_eqn(expr, a)
    assert(sol == -b)

def test_cyclic_solve ():
    a, b = map(lambda x: Tensor(x, rank=0), 'ab')
    assert(backward_sub([a + b], [], [a, b]) == (None, b))

def test_sol_without_recomputes ():
    a, b, c, d = map(lambda x: Tensor(x, rank=0), 'abcd')
    sol_dict = {a: b + c*d, b: c*d}
    ord_unk = [a, b]
    assert(sol_without_recomputes((sol_dict, ord_unk)) == (sol_dict, ord_unk))
    sol_dict = {a: b + c*d, b: c*d}
    ord_unk = [b, a]
    assert(sol_without_recomputes((sol_dict, ord_unk)) is None)
    sol_dict = {a: set([b + c*d]), b: set([c*d])}
    ord_unk = [b, a]
    assert(sol_without_recomputes((sol_dict, ord_unk)) is None)
    sol_dict = {a: set([b + c*d, b*d]), b: set([c*d])}
    ord_unk = [b, a]
    assert(sol_without_recomputes((sol_dict, ord_unk)) == \
           ({a: set([b*d]), b: set([c*d])}, ord_unk))
    sol_dict = {a: set([b + c*d, b*d]), b: set([c*d])}
    ord_unk = [a, b]
    assert(sol_without_recomputes((sol_dict, ord_unk)) == (sol_dict, ord_unk))
