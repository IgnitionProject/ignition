"""Implements the recurrence orthonoalization from conjugant gradients."""

from numpy import matrix

from ignition.dsl.flame import *
from ignition.utils import flatten_list

# Define the operation
def AR_RH_Op (A, R, H, X, O):
    return [X * H - X,
            A * R - R * H,
            T(R) * R - O]

def AR_RH_Inv(A, R, H, X, O):
    [A] = A
    [R_l, r_m, R_r] = R
    [[H_tl, h_tm, H_tr],
     [Th_ml, eta_mm, Th_mr],
     [_, h_bm, H_br]] = H
    [X_l, x_m, X_r] = X
    [[O_tl, _ , _],
     [_, omega_mm, _],
     [_, _, O_br]] = O
    eqns = [A * R_l - R_l * H_tl - r_m * Th_ml,
            T(R_l) * R_l - O_tl,
            T(r_m) * R_l,
            T(R_l) * r_m,
            T(r_m) * r_m - omega_mm
            ]
    if H_tl.shape == (2, 2) and Th_ml.shape == (1, 2):
        print "H_tl and Th_ml:", H_tl, Th_ml
        eqns.append(matrix([[T(e), one]]) * H_tl + matrix([[one]]) * Th_ml)
    if H_tl.shape == (1, 1) and Th_ml.shape == (1, 1):
        print "H_tl and Th_ml:", H_tl, Th_ml
        eqns.append(matrix([[T(e)]]) * H_tl + matrix([[one]]) * Th_ml)
    def unroll_mats(acc, eqn):
        if isinstance(eqn, matrix):
            return acc + flatten_list(eqn.tolist())
        else:
            return acc + [eqn]
    eqns = reduce(unroll_mats, eqns, [])
    return eqns, [e]

from ignition.flame.tensors.basic_operators import add_invertible
O_00 = Tensor("O_00", rank=2)
add_invertible(O_00)

def victor_solver(b4_eqns, aft_eqns, e_knowns):
    added = []
    A = Tensor("A", 2)
    R_0 = Tensor("R_0", 2)
    r_1 = Tensor("r_1", 1)
    O_00 = Tensor("O_00", 2)
    w_11 = Tensor("omicron_11", 0)
    for eqn in aft_eqns:
        if A in eqn:
            added.append((T(R_0) * eqn).expand().subs(T(R_0) * R_0, O_00))
            added.append((T(r_1) * eqn).expand().subs(T(r_1) * r_1, w_11))
    aft_eqns.extend(added)
    return tensor_solver(b4_eqns, aft_eqns, e_knowns)

# Define the Partition Objs
A = iterative_arg("A", rank=2, part_suffix="1x1")
R = iterative_arg("R", rank=2, part_suffix="1x3", arg_src="Computed")
H = iterative_arg("H", rank=2, part_suffix="H_3x3", arg_src="Computed")
X = iterative_arg ("X", rank=2, part_suffix="1x3", arg_src="Overwrite")
O = iterative_arg ("O", rank=2, part_suffix="Diag_3x3", arg_src="Computed")

# Generate the algorithm
generate(op=AR_RH_Op, loop_inv=AR_RH_Inv, solver=tensor_solver,
         inv_args=[A, R, H, X, O], filetype="text")
