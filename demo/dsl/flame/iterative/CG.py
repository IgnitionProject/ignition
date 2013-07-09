"""Implements the complete conjugant gradient examples."""

from numpy import matrix

from ignition.dsl.flame import *
from ignition.utils import flatten_list

# Define the operation
def CG_Op (A, X, P, I, U, J, D, R, O):
    return [X * (I + U) - P * D,
            A * P * D - R * (I - U),
            P * (I - J) - R,
            T(R) * R - O]

# Define the loop invariant
def CG_Inv (A, X, P, I, U, J, D, R, O):
    [A] = A
    [X_l, x_m, X_r] = X
    [P_l, p_m, P_r] = P
    [[I_tl, _, _],
     [_, o, _],
     [_, _, I_br]] = I
    [[U_tl, u_tm, U_tr],
     [_, _, t_u_mr],
     [_, _, U_br]] = U
    [[J_tl, _, _],
     [T_m_j_ml, _, _],
     [_, j_bm, J_br]] = J
    [[D_l, _, _],
     [_, d_m, _],
     [_, _, D_r]] = D
    [R_l, r_m, R_t] = R
    eqns = [A * P_l * D_l - R_l * (I_tl - J_tl) - r_m * T_m_j_ml,
            P_l * D_l - X_l * (I_tl - J_tl) - x_m * T_m_j_ml,
            P_l * (I_tl - U_tl) - R_l,
            - P_l * u_tm + p_m - r_m,
            T(R_l) * r_m,
            T(r_m) * R_l,
            T(P_l) * A * p_m]

    known = []
#            U_tr,
#            u_mm]

    print "U_tr:", U_tr
#    print "P_l:", P_l
#    print "I_U_tl:", I_tl
#    print "R_l:", R_l
#    print  "P_l * I_U_tl - R_l", pprint.pformat(P_l * I_tl - R_l)
    def unroll_mats(acc, eqn):
        if isinstance(eqn, matrix):
            return acc + flatten_list(eqn.tolist())
        else:
            return acc + [eqn]

    eqns = reduce(unroll_mats, eqns, [])
    return eqns, reduce(unroll_mats, known, [])

# Hold your nose
from ignition.flame.tensors.basic_operators import add_invertible
A = Tensor("A", rank=2)
P_0 = Tensor("P_0", rank=2)
add_invertible(T(P_0) * A * P_0)
add_invertible(T(P_0) * A ** 2 * P_0)


# Define the Partition Objs
A = iterative_arg("A", rank=2, part_suffix="1x1")
X = iterative_arg ("X", rank=2, part_suffix="1x3", arg_src="Overwrite")
P = iterative_arg ("P", rank=2, part_suffix="1x3", arg_src="Computed")
I = iterative_arg ("I", rank=2, part_suffix="I_3x3", arg_src="Computed")
U = iterative_arg ("U", rank=2, part_suffix="Upper_Bidiag_3x3", arg_src="Computed")
J = iterative_arg ("J", rank=2, part_suffix="J_3x3", arg_src="Computed")
D = iterative_arg ("D", rank=2, part_suffix="Diag_3x3", arg_src="Computed")
R = iterative_arg ("R", rank=2, part_suffix="1x3", arg_src="Computed")
O = iterative_arg ("O", rank=2, part_suffix="1x3", arg_src="Computed")


# Generate the algorithm
generate(op=CG_Op, loop_inv=CG_Inv, solver=tensor_solver,
         inv_args=[A, X, P, I, U, J, D, R, O], filetype="latex",
         solution_file="cg_updates.tex", logic_files="cg_logic")
