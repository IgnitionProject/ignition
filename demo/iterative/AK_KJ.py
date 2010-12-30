"""Simple demo of iterative update for AK = KJ


"""

from numpy import matrix

from ignition.flame import *

ZERO = Tensor('0', 2)
Zero = Tensor('0', 1)
zero = Tensor('0', 0)
One = Tensor('1', 1)
one = Tensor('1', 0)

# Define partition rules 
def it_part_1x3 (M):
    return [M.new(l_ind="L"), M.new(l_ind="m", rank=M.rank - 1), M.new(l_ind="R")]

def it_part_J (J):
    return [[J.new(l_ind="tl"), Zero, Zero],
            [T(J.new(l_ind="ml", rank=J.rank - 1)), Zero, Zero],
            [Zero, J.new(l_ind="bm", rank=J.rank - 1), J.new(l_ind="br")]]

def it_nopart (M):
    return [M]

# Define the repartition rules
def repartK (K, *args, **kws):
    ret_dict = {}
    [K_l, k_m, K_r] = K
    ret_dict[K_l] = matrix([[K_l.new(l_ind="0")]])
    ret_dict[k_m] = matrix([[k_m.new(l_ind="1")]])
    ret_dict[K_r] = matrix([[K_r.new(l_ind="2", rank=1), K_r.new(l_ind="3")]])
    return ret_dict

def repartJ (J):
    ret_dict = {}
    [[J_tl, _, _],
     [Tj_ml, _, _],
     [_, j_bm, J_br]] = J
    ret_dict[J_tl] = matrix([[J_tl.new(l_ind="00")]])
    ret_dict[Tj_ml] = matrix([[Tj_ml.new(l_ind="10")]])
    ret_dict[j_bm] = matrix([[one, zero],
                             [Zero, j_bm.new(l_ind="32")]])
    ret_dict[J_br] = matrix([[T(Zero)],
                             [J_br.new(l_ind="33")]])
    return ret_dict

def repartA (A):
    [A_inner] = A
    return {A_inner:matrix([A])}

# Define the fuse rules
def fuseK (K, *args, **kws):
    ret_dict = {}
    [K_l, k_m, K_r] = K
    ret_dict[K_l] = matrix([K_l.new(l_ind="0"), k_m.new(l_ind="1")])
    ret_dict[k_m] = matrix([K_r.new(l_ind="2", rank=1)])
    ret_dict[K_r] = matrix([K_r.new(l_ind="3")])
    return ret_dict

def fuseJ (J):
    ret_dict = {}
    [[J_tl, _, _],
     [Tj_ml, _, _],
     [_, j_bm, J_br]] = J
    ret_dict[J_tl] = matrix([[J_tl.new(l_ind="00"), Zero],
                             [Tj_ml.new(l_ind="10"), zero]])
    ret_dict[Tj_ml] = matrix([T(Zero), one])
    ret_dict[j_bm] = matrix([j_bm.new(l_ind="32")])
    ret_dict[J_br] = matrix([J_br.new(l_ind="33")])
    return ret_dict

def fuseA (A):
    [A_inner] = A
    return {A_inner:matrix([A])}

# Define the loop invariant
def AK_KJ_Rule (A, K, J):
    [A] = A
    [K_l, k_m, K_r] = K
    [[J_tl, _, _],
     [Tj_ml, _, _],
     [_, j_bm, J_br]] = J
    return flatten((A * K_l - K_l * J_tl - k_m * Tj_ml).tolist())


# Define the objects used in the PME
A = Tensor("A", rank=2)
K = Tensor("K", rank=2)
J = Tensor("J", rank=2)

# Define the Partition Objs
A = PObj(Tensor("A", rank=2), part_fun=it_nopart, repart_fun=repartA, fuse_fun=fuseA,
         arg_src=PObj.ARG_SRC.Input)
K = PObj(Tensor("K", rank=2), part_fun=it_part_1x3, repart_fun=repartK, fuse_fun=fuseK,
         arg_src=PObj.ARG_SRC.Output)
J = PObj(Tensor("J", rank=2), part_fun=it_part_J, repart_fun=repartJ, fuse_fun=fuseJ,
         arg_src=PObj.ARG_SRC.Computed)

# Generate the algorithm
generate("AK_KJ.out", loop_inv=AK_KJ_Rule, inv_args=[A, K, J],
         updater=tensor_updater)
