"""Implements the complete conjugant gradient examples."""

from numpy import matrix

from ignition.dsl.flame import *
from ignition.utils import flatten_list

# Define the operation
def CG_Op (A, X, P, I, U, J, D, R, W,Z):
    return [X * (I - J) - P * D,
            A * P * D - R * (I - J),
            P * (I - U) - R,
            T(R) * R - W, T(P) * A * P - Z ]

# Define the loop invariant
def CG_Inv (A, X, P, I, U, J, D, R, W,Z):
    [A] = A
    [X_l, x_m, X_r] = X
    [P_l, P_m, P_r] = P
    [[I_tl, _, _],
     [_, o, _],
     [_, _, I_br]] = I
    [[U_tl, U_tm, U_tr],
     [_, _, U_mr],
     [_, _, U_br]] = U
    [[J_tl, _ , _],
     [j_ml, _, _],
     [_, j_bm, J_br]] = J
    [[D_l, _, _],
     [_, D_m, _],
     [_, _, D_r]] = D
    [R_l, R_m, R_r] = R
    [W_l, W_m, W_r] = W
    [Z_l, Z_m, Z_r] = Z
    eqns = [
      R_l * J_tl + R_m * j_ml - R_l - A * P_l * D_l,
      P_l - P_l * U_tl - R_l,
      P_m - P_l * U_tm - R_m,
      T(R_l) * R_l - W_l,
      T(P_l) * A * P_l - Z_l,
      T(P_l) * A * P_m,
      T(P_m) * A * P_l,
      T(P_m) * A * P_m - Z_m, # without this it works fine
    ]

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
W = iterative_arg ("W", rank=2, part_suffix="1x3", arg_src="Computed")
Z = iterative_arg ("Z", rank=2, part_suffix="1x3", arg_src="Computed")


# Generate the algorithm
generate(op=CG_Op, loop_inv=CG_Inv, solver=tensor_solver,
         inv_args=[A, X, P, I, U, J, D, R, W,Z ], filetype="latex",
         solution_file="alg6.tex", logic_files="cg_logic")
