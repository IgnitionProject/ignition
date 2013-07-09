"""Implements testing routines for given iterative method solvers"""

import traceback
import sys

from functools import partial
from numpy import eye, dot, max, sqrt, zeros, ones
from numpy.linalg import solve
from pprint import pprint
from sympy.utilities.pytest import skip

from ignition.dsl.flame.tensors import all_back_sub, numpy_print, T, Tensor

TEST_NUM_SOLS = 1000
TEST_LEVELS = -1
ABS_RES = 1e-3

#b = random(100)
b = zeros(100)
b[48] = 1.0
#x0 = random(100)
x0 = zeros(100)
#x0 = ones(100)

def get_fd_poisson(n=100):
    A = 2 * eye(n)
    A[0][0] = 1
    A[n - 1][n - 1] = 1
    for i in xrange(1, n - 2):
        A[i + 1][i] = A[i][i + 1] = -1
#    b = random(n)
#    b = ones(n)
    return A, b

def cg_alg_driver(alg, n=100):
    A, b = get_fd_poisson(n)
    iters, x = alg(A, b, n)
    x_numpy = solve(A, b)
    diff = x - x_numpy
    l_inf = max(diff)
    l_2 = sqrt(dot(diff, diff))
#    assert(l_inf < 1e-10)
#    assert(l_2 < 1e-10)
    return iters, l_2, l_inf

def cg_alg_gold(A, b, n=100):
    """Standard cg algorithm for comparisons"""
    # Taken from Templates book
#    x_i = random(b.shape)
    x_i = zeros(b.shape)
    r_i = b - dot(A, x_i)
    rho_i_1 = 0
    for i in xrange(n):
        rho_i = dot(r_i, r_i)
        if i == 0:
            p_i = r_i
        else:
            beta_i = rho_i / rho_i_1
            p_i = r_i + beta_i * p_i
        q_i = dot(A, p_i)
        alpha_i = rho_i / dot(p_i, q_i)
        print "iteration %d, residual %.2e, alpha %.2e" \
            % (i, sqrt(sum([x ** 2 for x in r_i])), alpha_i)
        x_i = x_i + alpha_i * p_i
        r_i = r_i - alpha_i * q_i
        rho_i_1 = rho_i
        if sqrt(sum([r ** 2 for r in r_i ])) < ABS_RES:
            break
    return i, x_i

def cg_saad(A, b, n=100):
    """Saad CG algorithm"""
#    x_i = random(b.shape)
    x_i = zeros(b.shape)
    r_i = b - dot(A, x_i)
    z_i = r_i
    p_i = z_i
    s_i = dot(r_i, z_i)
    for i in xrange(n):
        v_i = dot(A, p_i)
        vAp = dot(v_i, dot(A, p_i))
        App = dot(dot(A, p_i), p_i)
        alpha_i = s_i / App
        s_i_1 = alpha_i ** 2 * vAp - s_i
        beta_i = s_i_1 / s_i
        s_i = s_i_1
        print "iteration %d, residual %.2e, alpha %.2e" \
            % (i, sqrt(sum([x ** 2 for x in r_i])), alpha_i)
        x_i = x_i + alpha_i * p_i
        r_i = r_i - alpha_i * dot(A, p_i)
        p_i = z_i - alpha_i * v_i + beta_i * p_i
        z_i = z_i - alpha_i * v_i
        if sqrt(sum([r ** 2 for r in r_i ])) < ABS_RES:
            break
    return i, x_i


def cg_saad_meurant(A, b, n=100):
    """Saad Meurant CG algorithm"""
#    x_i = random(b.shape)
    x_i = zeros(b.shape)
    r_i = b - dot(A, x_i)
    z_i = r_i
    p_i = z_i
    for i in xrange(n):
        q_i = dot(A, p_i)
        v_i = q_i
        vAp = dot(v_i, dot(A, p_i))
        App = dot(dot(A, p_i), p_i)
        rz = dot(r_i, z_i)
        alpha_i = rz / App
        s_i = alpha_i ** 2 * vAp - rz
        beta_i = s_i / rz
        print "iteration %d, residual %.2e, alpha %.2e" \
            % (i, sqrt(sum([x ** 2 for x in r_i])), alpha_i)
        x_i = x_i + alpha_i * p_i
        r_i = r_i - alpha_i * q_i
        p_i = z_i - alpha_i * v_i + beta_i * p_i
        z_i = z_i - alpha_i * v_i
        if sqrt(sum([r ** 2 for r in r_i ])) < ABS_RES:
            break
    return i, x_i

def sols_to_co(sols):
    sol, order = sols
    src = ""
    q = sol.keys()
    for var in order:
        src = "%s = %s\n" % (str(var), numpy_print(sol[var])) \
            + src
        q.remove(var)
    reject = []
    len_reject = 0
    while len(q) != 0 or len(reject) != 0:
        if len(q) == 0:
            if len_reject == len(reject):
                break
            len_reject = len(reject)
            q = reject
            reject = []
        var = q.pop(0)
        rejected = False
        for k in q:
            if var in sol[k]:
                reject.append(var)
                rejected = True
                break
        if rejected:
            continue
        src = "%s = %s\n" % (str(var), numpy_print(sol[var])) + src
    if len(reject) != 0:
        raise ValueError("Sols has circular dependency,\n%s" % \
                         str((reject, sol)))
    return compile(src, "<sols_to_co>", "exec")

def cg_alg_from_sols(sols, A, b, n=101):
    p_2 = None
    x_2 = None
    r_2 = None
    q_2 = None
    pi_2 = None
#    x_1 = random(b.shape)
#    x_1 = zeros(b.shape)
    x_1 = x0
    r_1 = b - dot(A, x_1)
    p_1 = r_1
    q_1 = dot(A, p_1)
    delta_1 = 0
    pi_1 = dot(p_1, dot(A, p_1))
    co = sols_to_co(sols)
    for i in xrange(n):
        exec(co)
        p_1 = p_2
        x_1 = x_2
        r_1 = r_2
        q_1 = q_2
        pi_1 = pi_2
        if sqrt(sum([r ** 2 for r in r_1 ])) < ABS_RES:
            break
    return i, x_1

def run_cg_algorithms(cg_eqns, knowns):
    print("Solving for CG updates.")
    cg_sols = all_back_sub(cg_eqns, knowns, levels=TEST_LEVELS)
    tot_test = min(len(cg_sols), TEST_NUM_SOLS)
    print("Found %d solutions, testing the first %d" \
          % (len(cg_sols), tot_test))
    for i in xrange(tot_test):
        print "=" * 80
        print "Algorithm %d:" % i
        pprint(cg_sols[i][0])
        try:
            iters, l2, linf = cg_alg_driver(partial(cg_alg_from_sols, cg_sols[i]))
            print "-" * 80
            print "iters = %d" % iters
            print "l2 error = %.2e" % l2
            print "linf error = %.2e" % linf
        except Exception as e:
            print "-" * 80
            print "Algorithm failed"
            print e
            traceback.print_exc(file=sys.stdout)
        print "=" * 80

def test_reg_cg():
    delta_1, mu_12 = map(lambda x: Tensor(x, rank=0), ['delta_1', 'mu_12'])
    r_1, r_2, p_1, p_2, x_1, x_2 = map(lambda x: Tensor(x, rank=1), \
                                   ['r_1', 'r_2', 'p_1', 'p_2', 'x_1', 'x_2'])
    A = Tensor('A', rank=2)

    # Specify which variables are known
    knowns = [p_1, r_1, x_1, A]

    # Specify the CG eqns (coming from a 4x4 PME)
    cg_eqns = [delta_1 * A * p_1 - r_1 + r_2,
               p_2 - r_2 + p_1 * mu_12,
               x_2 - x_1 - delta_1 * p_1,
               T(r_1) * r_2,
               T(p_1) * A * p_2,
               ]
    run_cg_algorithms(cg_eqns, knowns)

def test_expanded_cg():
    skip("Test takes too long")
    delta_1, mu_12 = map(lambda x: Tensor(x, rank=0), ['delta_1', 'mu_12'])
    r_1, r_2, q_1, q_2, p_1, p_2, x_1, x_2 = map(lambda x: Tensor(x, rank=1), \
        ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 'x_1', 'x_2'])
    A = Tensor('A', rank=2)

    # Specify which variables are known
    knowns = [p_1, q_1, r_1, x_1, A]

    # Specify the CG eqns (coming from a 4x4 PME)
    cg_eqns = [delta_1 * q_1 - r_1 + r_2,
               delta_1 * A * p_1 - r_1 + r_2,
               q_2 - A * p_2,
               q_2 - A * r_2 + q_1 * mu_12,
               p_2 - r_2 + p_1 * mu_12,
               x_2 - x_1 - delta_1 * p_1,
               T(r_1) * r_2,
               T(p_1) * q_2,
               ]
    run_cg_algorithms(cg_eqns, knowns)

def test_chronos_cg():
    skip("Test takes too long")
    delta_1, omega_2, pi_1, pi_2, mu_12 = map(lambda x: Tensor(x, rank=0), \
        ['delta_1', 'omega_2', 'pi_1', 'pi_2', 'mu_12'])
    r_1, r_2, q_1, q_2, p_1, p_2, x_1, x_2 = map(lambda x: Tensor(x, rank=1), \
        ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 'x_1', 'x_2'])
    A, R_0, P_0 = map(lambda x: Tensor(x, rank=2), ['A', 'R_0', 'P_0'])

    # Specify which variables are known
    knowns = [pi_1, p_1, r_1, q_1, x_1, A, R_0, P_0]

    # Now try the chronos variant and repeat.
    chronos_eqns = [r_2 - r_1 - delta_1 * q_1,
                q_2 - A * p_2,
                p_2 - r_2 + p_1 * mu_12,
                q_2 - A * r_2 + q_1 * mu_12,
                x_2 - x_1 - delta_1 * p_1,
                omega_2 - T(r_2) * r_2,
                pi_2 - T(p_2) * A * p_2,
                T(R_0) * r_2,
                T(r_1) * r_2,
                T(P_0) * A * p_2,
                T(p_1) * A * p_2,
                T(p_2) * A * p_2 - T(r_2) * A * r_2 + T(mu_12) * pi_1 * mu_12,
                ]
    run_cg_algorithms(chronos_eqns, knowns)

def test_cg_gold():
    iters, l2, linf = cg_alg_driver(cg_alg_gold)
    print l2, linf
#    assert(l2 < 1e-10)
#    assert(linf < 1e-10)

def test_cg_saad_meurant():
    iters, l2, linf = cg_alg_driver(cg_saad_meurant)
    print l2, linf
#    assert(l2 < 1e-10)
#    assert(linf < 1e-10)

def test_cg_saad():
    iters, l2, linf = cg_alg_driver(cg_saad)
    print l2, linf

if __name__ == "__main__":
#    test_reg_cg()
    test_expanded_cg()
#    test_chronos_cg()
#    test_cg_saad()
#    test_cg_saad_meurant()
#    test_cg_gold()

