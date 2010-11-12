"""Implements testing routines for given iterative method solvers"""

from numpy import eye, dot, max, sqrt
from numpy.random import random
from numpy.linalg import solve
from pprint import pprint


from ignition.symbolics.tensors import numpy_print, T, Tensor
from ignition.symbolics.tensor_solvers import all_back_sub

TEST_NUM_SOLS = 9

def cg_alg_gold(A, b, n=100):
    """Standard cg algorithm for comparisons"""
    # Taken from Templates book
    x_i = random(b.shape)
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
        x_i = x_i + alpha_i * p_i
        r_i = r_i - alpha_i * q_i
        rho_i_1 = rho_i
    return x_i

def sols_to_co(sols):
    sol, order = sols
    src = ""
    q = sol.keys()
    for var in order:
#        print "converting %s = %s" % (str(var), str(sol[var]))
        src = "%s = %s\n" % (str(var), numpy_print(sol[var])) \
            + src
        q.remove(var)
    reject = []
    len_reject = 0
    while len(q) != 0 or len(reject) != 0:
#        print "front of loop"
#        print len_reject, len(q), len(reject)
#        print q
#        print reject
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
#        print "here"
#        print "end of loop"
#        print len_reject, len(q), len(reject)
#        print q
#        print reject
#        print len(q) != 0, len(reject) != 0, len_reject != len(reject)
#        print len(q) != 0 and (len(reject) != 0 or len_reject != len(reject))
        if rejected:
            continue
        src = "%s = %s\n" % (str(var), numpy_print(sol[var])) + src

#    print "out of loop"
#    print len_reject, len(q), len(reject)
#    print q
#    print reject
#    print src
    if len(reject) != 0:
        raise ValueError("Sols has circular dependency,\n%s" % str((reject, sol)))
#    print "sols_to_co, source code\n", src
    return compile(src, "<sols_to_co>", "exec")

def cg_alg_from_sols(sols, A, b, n=100):
    x_1 = random(b.shape)
    r_1 = b - dot(A, x_1)
    p_1 = r_1
    x_2 = x_1
    co = sols_to_co(sols)
    for _ in xrange(n):
        exec(co)
        p_1 = p_2
        x_1 = x_2
        r_1 = r_2
    return x_2


def cg_alg_0(A, b, n=100):
    x_1 = random(b.shape)
    r_1 = b - dot(A, x_1)
    p_1 = r_1
    x_2 = x_1
    for _ in xrange(n):
        delta_1 = dot(1.0 / dot(r_1, dot(A, p_1)), dot(r_1, r_1))
        x_2 = dot(1.0 / dot(r_1, dot(A, p_1)), dot(dot(r_1, r_1), p_1)) + x_1
        r_2 = r_1 - dot(delta_1, dot(A, p_1))
        mu_12 = dot(1.0 / dot((dot((p_1).transpose(), A)).transpose(), p_1), dot((dot((p_1).transpose(), A)).transpose(), r_2))
        p_2 = -dot(mu_12, p_1) + r_2
        p_1 = p_2
        x_1 = x_2
        r_1 = r_2
    return x_2

def test_cg_algorithms():
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
    print("Solving for CG updates.")
    cg_sols = all_back_sub(cg_eqns, knowns, levels=3)
    print("Found %d solutions, testing the first %d" \
          % (len(cg_sols), min(len(cg_sols), TEST_NUM_SOLS)))
    n = 100
    A, b = get_fd_poisson(n)
    x_numpy = solve(A, b)
    for i in xrange(TEST_NUM_SOLS):
        x = cg_alg_from_sols(cg_sols[i], A, b, n)
        diff = x - x_numpy
        print "=" * 80
        print "Algorithm %d:" % i
        pprint(cg_sols[i][0])
        print "-" * 80
        print "l2 error = %.2e" % sqrt(dot(diff, diff))
        print "=" * 80

def get_fd_poisson(n=100):
    A = 2 * eye(n)
    A[0][0] = 1
    A[n - 1][n - 1] = 1
    for i in xrange(1, n - 2):
        A[i + 1][i] = A[i][i + 1] = -1
    b = random(n)
    return A, b

def cg_alg_tester(alg, n=100):
    A, b = get_fd_poisson(n)
    x = alg(A, b, n)
    x_numpy = solve(A, b)
    diff = x - x_numpy
    assert(max(diff) < 1e-10)
    assert(sqrt(dot(diff, diff)) < 1e-10)

def test_cg_gold():
    cg_alg_tester(cg_alg_gold)

def test_cg_0():
    cg_alg_tester(cg_alg_0)

if __name__ == "__main__":
    test_cg_algorithms()
#    test_cg_0()
