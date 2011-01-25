"""Example of deriving updates for several CG algorithms"""

import pprint
import sys

from ignition import *
from ignition.flame.tensors.solvers import backward_sub

SHOW_NUM_SOLS = 3

# First define the variables 
delta_1, omega_2, pi_1, pi_2, gamma_2, mu_12 = \
    map(lambda x: Tensor(x, rank=0),
        ['delta_1', 'omega_2', 'pi_1', 'pi_2', 'gamma_2', 'mu_12'])
r_1, r_2, q_1, q_2, p_1, p_2, s_1, s_2, u_02, x_1, x_2 = \
    map(lambda x: Tensor(x, rank=1),
        ['r_1', 'r_2', 'q_1', 'q_2', 'p_1', 'p_2', 's_1', 's_2', 'u_02',
         'x_1', 'x_2'])
A, R_0, P_0 = map(lambda x: Tensor(x, rank=2), ['A', 'R_0', 'P_0'])

# Specify which variables are known
knowns = [p_1, r_1, q_1, x_1, pi_1, A, R_0, P_0]

def cg ():
    # Specify the CG eqns (coming from a 4x4 PME)
    cg_eqns = [delta_1 * A * p_1 - r_1 + r_2,
               p_2 - r_2 + p_1 * mu_12,
               x_2 - x_1 - delta_1 * p_1,
               T(r_1) * r_2,
               T(p_1) * A * p_2,
               ]
    # Extras r_1*T(j_10) - R_0*(-J_00 + I_00) + A*P_0*D_00,
    #       P_0*D_00 + x_1*T(j_10) - X_0*(-J_00 + I_00),
    #       -R_0 + P_0*(I_00 + U_00),
    #      -r_1 + (1_0 + su_11)*p_1 + P_0*u_01,


    #Solve and give information about solutions
    print("Solving for CG updates.")
    print "CG eqns:", pprint.pformat(cg_eqns)
    print"knowns:", pprint.pformat(knowns)
    sols = all_back_sub(cg_eqns, knowns, levels=3)
    print_sols(sols)

def chronos ():
    # Now try the chronos variant and repeat.
    chronos_eqns = [r_2 - r_1 - delta_1 * q_1,
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
    print("Solving for Chronos-CG updates.")
    sols = all_back_sub(chronos_eqns, knowns, levels=3)
    print_sols(sols)

def print_sols(sols):
    print("Found %d solutions, printing the first %d" \
          % (len(sols), min(len(sols), SHOW_NUM_SOLS)))
    for i in xrange(min(len(sols), SHOW_NUM_SOLS)):
        print("-"*80)
        print("Solution %d, from ordering %s" % (i, str(sols[i][1])))
        pprint.pprint(sols[i][0])
    print("-"*80)

def cg_demo_eqns ():
    D_00, J_00, I_00, U_00, X_0 = map(lambda x: Tensor(x, rank=2),
                           ["D_00", "J_00", "I_00", "U_00", "X_0"])
    j_10, u_01, u_02 = map(lambda x: Tensor(x, rank=1),
                           ["j_10", "u_01", "u_02"])
    delta_11, su_12 = map(lambda x: Tensor(x, rank=0),
                          ["delta_11", "su_12"])
    cg_2 = [ \
          r_1 * T(j_10) - R_0 * (-J_00 + I_00) + A * P_0 * D_00,
          - r_1 - r_2 + delta_11 * A * p_1,
          P_0 * D_00 + x_1 * T(j_10) - X_0 * (-J_00 + I_00),
          - x_1 - x_2 + delta_11 * p_1,
          - R_0 + P_0 * (-U_00 + I_00),
          - r_1 - P_0 * u_01 + p_1,
          - r_2 - P_0 * u_02 - su_12 * p_1 + p_2,
          T(R_0) * r_2,
          (T(r_1) * r_2),
          T(r_2) * R_0,
          (T(r_2) * r_1),
          T(P_0) * A * p_2,
          (T(p_1) * A * p_2),
          - R_0 * (-J_00 + I_00) - r_1 * T(j_10) + A * P_0 * D_00,
          P_0 * D_00 - X_0 * (-J_00 + I_00) - x_1 * T(j_10),
          - R_0 + P_0 * (-U_00 + I_00),
          - r_1 - P_0 * u_01 + p_1,
          T(R_0) * r_1,
          T(r_1) * R_0,
          T(P_0) * A * p_1,
            ]
    cg_1 = [-r_1 - r_2 + delta_11 * A * p_1,
            - x_1 - x_2 + delta_11 * p_1,
            - r_2 + p_2 ]
    knowns = set([U_00, p_1, X_0, u_01, x_1, I_00, j_10, D_00, R_0, r_1, A,
                  P_0, J_00 ])
    unknowns = [p_2, su_12, u_02, x_2, r_2, delta_11]
    print("Solving for CG-Demo updates.")
#    sols = all_back_sub(cg_2, knowns, levels= -1)
#    print "solve_vec_eqn(T(P_0)*A*r_2 + T(P_0)*A*P_0*u_02, u_02)"
#    print solve_vec_eqn(T(P_0) * A * r_2 + T(P_0) * A * P_0 * u_02, u_02)
#    print_sols(sols)
    sol = backward_sub(cg_2, knowns, unknowns, False, True)
    print "Sol:", pprint.pformat(sol)
if __name__ == "__main__":
    cg_demo_eqns()
#    cg()
