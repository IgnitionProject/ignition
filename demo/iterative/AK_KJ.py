"""Simple demo of iterative update for AK = KJ


"""

from ignition.flame import *

ZERO = Tensor('0', 2)
Zero = Tensor('0', 1)
zero = Tensor('0', 0)
One = Tensor('1', 1)
one = Tensor('1', 0)

# Define partition rules 
def it_part_1x3 (M):
    return [M.new(ind="L"), M.new(ind="m", rank=M.rank() - 1), M.new(ind="R")]

def it_part_J (J):
    return [[J.new(ind="tl"), Zero, Zero],
            [J.new(ind="ml", rank=J.rank() - 1, transpose=True), Zero, Zero],
            [Zero, J.new(ind="bm", rank=J.rank() - 1), J.new(ind="br")]]

def it_nopart (M):
    return [M]

# Define the repartition rules
def repartK (K, *args, **kws):
    ret_dict = {}
    [K_l, k_m, K_r] = K
    ret_dict[K_l] = [[K_l.new(ind="0")]]
    ret_dict[k_m] = [[k_m.new(ind="1")]]
    ret_dict[K_r] = [[K_r.new(ind="2", rank=1), K_r.new(ind="3")]]
    return ret_dict

def repartJ (J):
    ret_dict = {}
    [[J_tl, _, _],
     [Tj_ml, _, _],
     [_, j_bm, J_br]] = J
    ret_dict[J_tl] = [[J_tl.new(ind="00")]]
    ret_dict[Tj_ml] = [[T(Tj_ml.new(ind="10"))]]
    ret_dict[j_bm] = [[one, zero],
                      [Zero, j_bm.new(ind="32")]]
    ret_dict[J_br] = [[T(Zero)],
                      [J_br.new(ind="33")]]
    return ret_dict

def repartA (A):
    A_inner = A
    return {A_inner:[A]}

# Define the fuse rules
def fuseK (K, *args, **kws):
    ret_dict = {}
    [K_l, k_m, K_r] = K
    ret_dict[K_l] = [K_l.new(ind="0"), k_m.new(ind="1")]
    ret_dict[k_m] = [K_r.new(ind="2", rank=1)]
    ret_dict[K_r] = [K_r.new(ind="3")]
    return ret_dict

def fuseJ (J):
    ret_dict = {}
    [[J_tl, _, _],
     [Tj_ml, _, _],
     [_, j_bm, J_br]] = J
    ret_dict[J_tl] = [[J_tl.new(ind="00"), Zero],
                      [T(Tj_ml.new(ind="10", transpose=True)), zero]]
    ret_dict[Tj_ml] = [T(Zero), one]
    ret_dict[j_bm] = [j_bm.new(ind="32")]
    ret_dict[J_br] = [J_br.new(ind="33")]
    return ret_dict

def fuseA (A):
    A_inner = A
    return {A_inner:[A]}

# Define the loop invariant
def AK_KJ_Rule (A, K, J):
    [A] = A
    [K_l, k_m, K_r] = K
    [[J_tl, _, _],
     [Tj_ml, _, _],
     [_, j_bm, J_br]] = J
    return flatten((A * K_l - K_l * J_tl + k_m * Tj_ml).tolist())


# Define the objects used in the PME
A = Tensor("A", rank=2)
K = Tensor("K", rank=2)
J = Tensor("J", rank=2)

# Define the Partition Objs
A = PObj(Tensor("A", rank=2), part=it_nopart, repart=repartA, fuse=fuseA)
K = PObj(Tensor("K", rank=2), part=it_part_1x3, repart=repartK, fuse=fuseK)
J = PObj(Tensor("J", rank=2), part=it_part_J, repart=repartJ, fuse=fuseJ)

# Generate the algorithm
generate("AK_KJ.out", loop_inv=AK_KJ_Rule, inv_args=[A, K, J],
         updater=tensor_updater)
