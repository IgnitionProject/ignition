"""Simple demo of iterative update for AK = KJ"""

from numpy import matrix

from ignition.dsl.flame import *
from ignition.utils import flatten

# Define the operation
def AK_KJ_Op (A, K, J):
    return A * K - K * J

# Define the loop invariant
def AK_KJ_Rule (A, K, J):
    [A] = A
    [K_l, k_m, K_r] = K
    [[J_tl, _, _],
     [Tj_ml, _, _],
     [_, j_bm, J_br]] = J
    op = (A * K_l - K_l * J_tl - k_m * Tj_ml)
    if type(op) is matrix:
        op = op.tolist()
    if type(op) is list:
        op = flatten(op)
    return op, []

# Define the Partition Objs
A = PObj(Tensor("A", rank=2),
         part_fun=Part_1x1(),
         repart_fun=Repart_1x1(),
         fuse_fun=Fuse_1x1(),
         arg_src=PObj.ARG_SRC.Input)
K = PObj(Tensor("K", rank=2),
         part_fun=Part_1x3(),
         repart_fun=Repart_1x3(),
         fuse_fun=Fuse_1x3(),
         arg_src=PObj.ARG_SRC.Output)
J = PObj(Tensor("J", rank=2),
         part_fun=Part_J_3x3(),
         repart_fun=Repart_J_3x3(),
         fuse_fun=Fuse_J_3x3(),
         arg_src=PObj.ARG_SRC.Computed)

# Generate the algorithm
#generate(op=AK_KJ_Op, loop_inv=AK_KJ_Rule, inv_args=[A, K, J],
#         updater=tensor_updater, filetype="latex")
generate(op=AK_KJ_Op, loop_inv=AK_KJ_Rule, inv_args=[A, K, J],
         solver=tensor_solver, filetype="text")
