
"""Implements the complete conjugant gradient examples."""

from numpy import matrix

from ignition.flame import *
from ignition.utils import flatten_list

# Define the operation
def CG_Op ( A,R,P,D,I,J,JI,U,W,Z, ):
    return [A * P * D - R * (I - J),
            P * (I - U) - R,
            T(R) * R - W, T(P) * A * P - Z ]

# Define the loop invariant
def CG_Inv ( A,R,P,D,I,J,JI,U,W,Z, ):
    [ A, ] = A
    [ R_l,R_m,R_r, ] = R
    [ P_l,P_m,P_r, ] = P
    [ [ D_l,_,_, ], [ _,D_m,_, ], [ _,_,D_r, ], ] = D
    [ [ I_tl,_,_, ], [ _,I_ml,_, ], [ _,_,I_br, ], ] = I
    [ [ J_tl,_,_, ], [ j_ml,_,_, ], [ _,j_bm,J_br, ], ] = J
    [ [ JI_tl,JI_tm,JI_tr, ], [ JI_ml,JI_mm,JI_mr, ], [ JI_bl,JI_bm,JI_br, ], ] = JI
    [ [ U_tl,U_tm,U_tr, ], [ _,U_mm,U_mr, ], [ _,_,U_br, ], ] = U
    [ [ W_l,_,_, ], [ _,W_m,_, ], [ _,_,W_r, ], ] = W
    [ [ Z_l,_,_, ], [ _,Z_m,_, ], [ _,_,Z_r, ], ] = Z
    eqns = [
     I_tl - J_tl - JI_tl ,
     j_ml - JI_ml ,
     R_l * J_tl + R_m * j_ml - R_l - A * P_l * D_l ,
     R_l * JI_tl + R_m * JI_ml - A * P_l * D_l ,
     P_l - R_l ,
     T(R_l) * R_l - W_l ,
     T(P_l) * A * P_l - Z_l ,
    ]

    known = []

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
A = iterative_arg("A",rank=2, part_suffix="1x1", arg_src="Input")
R = iterative_arg("R",rank=2, part_suffix="1x3", arg_src="Overwrite")
P = iterative_arg("P",rank=2, part_suffix="1x3", arg_src="Computed")
D = iterative_arg("D",rank=2, part_suffix="Diag_3x3", arg_src="Computed")
I = iterative_arg("I",rank=2, part_suffix="I_3x3", arg_src="Computed")
J = iterative_arg("J",rank=2, part_suffix="J_3x3", arg_src="Computed")
JI = iterative_arg("JI",rank=2, part_suffix="3x3", arg_src="Computed")
U = iterative_arg("U",rank=2, part_suffix="Upper_3x3", arg_src="Computed")
W = iterative_arg("W",rank=2, part_suffix="Diag_3x3", arg_src="Computed")
Z = iterative_arg("Z",rank=2, part_suffix="Diag_3x3", arg_src="Computed")

# Generate the algorithm
generate(op=CG_Op, loop_inv=CG_Inv, solver=tensor_solver,
         inv_args=[A,R,P,D,I,J,JI,U,W,Z,], filetype="latex",
         solution_file="alg1.in", logic_files="cg_logic")
