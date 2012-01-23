"""Partition rules for iterative methods"""

from numpy import matrix

from basic_operators import T
from constants import one, ZERO, Zero, zero
from prules import TensorPartRule, TensorRepartFuseRule


class Part_1x1 (TensorPartRule):
    shape = (1, 1)
    _latex_head = "\FLAOneByOne"
    def __call__ (self, M):
        return [M]

class Repart_1x1 (TensorRepartFuseRule):
    shape = (1, 1)
    reshape = (1, 1)
    _latex_head = "\FLAOneByOne"
    def __call__ (self, M):
        return {M[0]:matrix(M)}

Fuse_1x1 = Repart_1x1

class Part_1x3 (TensorPartRule):
    shape = (1, 3)
    _latex_head = "\FLAOneByThree"
    def __call__ (self, M):
        return [M.update(l_ind="L"), M.update(l_ind="m", rank=M.rank - 1),
                M.update(l_ind="R")]

class Repart_1x3 (TensorRepartFuseRule):
    shape = (1, 3)
    reshape = (1, 4)
    _latex_head = "\FLAOneByFour"
    def __call__ (self, M):
        ret = {}
        [M_l, m_m, M_r] = M
        ret[M_l] = matrix([[M_l.update(l_ind="0")]])
        ret[m_m] = matrix([[m_m.update(l_ind="1")]])
        ret[M_r] = matrix([[M_r.update(l_ind="2", rank=1), M_r.update(l_ind="3")]])
        return ret

class Fuse_1x3 (TensorRepartFuseRule):
    shape = (1, 3)
    reshape = (1, 4)
    _latex_head = "\FLAOneByFour"
    def __call__ (self, M):
        ret = {}
        [M_l, m_m, M_r] = M
        ret[M_l] = matrix([M_l.update(l_ind="0"), m_m.update (l_ind="1")])
        ret[m_m] = matrix([M_r.update(l_ind="2", rank=1)])
        ret[M_r] = matrix([M_r.update(l_ind="3")])
        return ret

class Part_3x3 (TensorPartRule):
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, M):
        return \
          [[M.update(l_ind="tl"), M.update(l_ind="tm", rank=1), M.update(l_ind="tr")],
           [T(M.update(l_ind="ml", rank=1)), M.update(l_ind="mm", rank=0), T(M.update(l_ind="mr", rank=1))],
           [M.update(l_ind="bl"), M.update(l_ind="bm", rank=1), M.update(l_ind="br")]]

class Repart_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, M):
        ret = {}
        [[M_tl, m_tm, M_tr],
         [T_m_ml, mu_mm, T_m_mr],
         [M_bl, m_bm, M_br]] = M

        ret[M_tl] = matrix([[M_tl.update(l_ind="00")]])
        ret[m_tm] = matrix([[m_tm.update(l_ind="01")]])
        ret[M_tr] = matrix([[m_tm.update(l_ind="02"), M_tr.update(l_ind="03")]])

        ret[T_m_ml] = matrix([[T_m_ml.update(l_ind="10")]])
        ret[mu_mm] = matrix([[mu_mm.update(l_ind="11")]])
        ret[T_m_mr] = matrix([[mu_mm.update(l_ind="12"), T_m_mr.update(l_ind="13")]])

        ret[M_bl] = matrix([[T_m_ml.update(l_ind="20")],
                            [M_bl.update(l_ind="30")]])
        ret[m_bm] = matrix([[mu_mm.update(l_ind="21")],
                            [m_bm.update(l_ind="31")]])
        ret[M_br] = matrix([[mu_mm.update(l_ind="22"), T_m_mr.update(l_ind="23")],
                            [m_bm.update(l_ind="32"), M_br.update(l_ind="33")]])
        return ret

class Fuse_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, M):
        ret = {}
        [[M_tl, m_tm, M_tr],
         [T_m_ml, mu_mm, T_m_mr],
         [M_bl, m_bm, M_br]] = M

        ret[M_tl] = matrix([[M_tl.update(l_ind="00"), m_tm.update(l_ind="01")],
                            [T_m_ml.update(l_ind="10"), mu_mm.update(l_ind="11")]])
        ret[m_tm] = matrix([[m_tm.update(l_ind="02")],
                            [mu_mm.update(l_ind="12")]])
        ret[M_tr] = matrix([[M_tr.update(l_ind="03")],
                            [T_m_mr.update(l_ind="13")]])

        ret[T_m_ml] = matrix([[T_m_ml.update(l_ind="20"), mu_mm.update(l_ind="21")]])
        ret[mu_mm] = matrix([[mu_mm.update(l_ind="22")]])
        ret[T_m_mr] = matrix([[T_m_mr.update(l_ind="23")]])

        ret[M_bl] = matrix([[M_bl.update(l_ind="30"), m_bm.update(l_ind="31")]])
        ret[m_bm] = matrix([[m_bm.update(l_ind="32")]])
        ret[M_br] = matrix([[M_br.update(l_ind="33")]])
        return ret

class Part_Upper_3x3 (TensorPartRule):
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, U):
        return \
          [[U.update(l_ind="tl"), U.update(l_ind="tm", rank=1), U.update(l_ind="tr")],
           [T(Zero), zero, T(U.update(l_ind="mr", rank=1))],
           [ZERO, Zero, U.update(l_ind="br")]]

class Repart_Upper_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, U):
        ret = {}
        [[U_tl, u_tm, U_tr],
         [_, _, T_u_mr],
         [_, _, U_br]] = U

        ret[U_tl] = matrix([[U_tl.update(l_ind="00")]])
        ret[u_tm] = matrix([[u_tm.update(l_ind="01")]])
        ret[U_tr] = matrix([[u_tm.update(l_ind="02"), U_tr.update(l_ind="03")]])

        ret[T_u_mr] = matrix([[u_tm.update(l_ind="12", rank=0),
                                T_u_mr.update(l_ind="13")]])

        ret[U_br] = matrix([[zero, T_u_mr.update(l_ind="23")],
                            [Zero, U_br.update(l_ind="33")]])
        return ret

class Fuse_Upper_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, U):
        ret = {}
        [[U_tl, u_tm, U_tr],
         [_, _, T_u_mr],
         [_, _, U_br]] = U

        ret[U_tl] = matrix([[U_tl.update(l_ind="00"), u_tm.update(l_ind="01")],
                            [T(Zero), zero]])
        ret[u_tm] = matrix([[u_tm.update(l_ind="02")],
                            [u_tm.update(l_ind="12", rank=0)]])
        ret[U_tr] = matrix([[U_tr.update(l_ind="03")],
                            [T_u_mr.update(l_ind="13")]])

        ret[T_u_mr] = matrix([[T_u_mr.update(l_ind="23")]])

        ret[U_br] = matrix([[U_br.update(l_ind="33")]])
        return ret

class Part_Upper_Bidiag_3x3 (TensorPartRule):
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, U):
        return \
          [[U.update(l_ind="tl"), U.update(l_ind="tm", rank=1), ZERO],
           [T(Zero), zero, T(U.update(l_ind="mr", rank=1))],
           [ZERO, Zero, U.update(l_ind="br")]]

class Repart_Upper_Bidiag_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, U):
        ret = {}
        [[U_tl, u_tm, _],
         [_, _, T_u_mr],
         [_, _, U_br]] = U

        ret[U_tl] = matrix([[U_tl.update(l_ind="00")]])
        ret[u_tm] = matrix([[u_tm.update(l_ind="01")]])

        ret[T_u_mr] = matrix([[u_tm.update(l_ind="12", rank=0),
                                T(Zero)]])

        ret[U_br] = matrix([[zero, T_u_mr.update(l_ind="23")],
                            [Zero, U_br.update(l_ind="33")]])
        return ret

class Fuse_Upper_Bidiag_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, U):
        ret = {}
        [[U_tl, u_tm, _],
         [_, _, T_u_mr],
         [_, _, U_br]] = U

        ret[U_tl] = matrix([[U_tl.update(l_ind="00"), u_tm.update(l_ind="01")],
                            [T(Zero), zero]])
        ret[u_tm] = matrix([[Zero],
                            [u_tm.update(l_ind="12", rank=0)]])

        ret[T_u_mr] = matrix([[T_u_mr.update(l_ind="23")]])

        ret[U_br] = matrix([[U_br.update(l_ind="33")]])
        return ret

class Part_Diag_3x3 (TensorPartRule):
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, D):
        return \
          [[D.update(l_ind="tl"), Zero, ZERO],
           [T(Zero), D.update(l_ind="mm", rank=0), T(Zero)],
           [ZERO, Zero, D.update(l_ind="br")]]

class Repart_Diag_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, D):
        ret = {}
        [[D_tl, _, _],
         [_, delta_mm, _],
         [_, _, D_br]] = D
        ret[D_tl] = matrix([[D_tl.update(l_ind="00")]])
        ret[delta_mm] = matrix([[delta_mm.update(l_ind="11")]])
        ret[D_br] = matrix([[delta_mm.update(l_ind="22"), T(Zero)],
                            [Zero, D_br.update(l_ind="33")]])
        return ret

class Fuse_Diag_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, D):
        ret = {}
        [[D_tl, _, _],
         [_, delta_mm, _],
         [_, _, D_br]] = D
        ret[D_tl] = matrix([[D_tl.update(l_ind="00"), Zero],
                            [T(Zero), delta_mm.update(l_ind="11")]])
        ret[delta_mm] = matrix([[delta_mm.update(l_ind="22")]])
        ret[D_br] = matrix([[D_br.update(l_ind="33")]])
        return ret

class Part_I_3x3 (TensorPartRule):
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, I):
        return \
          [[I.update(l_ind="tl"), Zero, ZERO],
           [T(Zero), one, T(Zero)],
           [ZERO, Zero, I.update(l_ind="br")]]

class Repart_I_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, I):
        ret = {}
        [[I_tl, _, _],
         [_, o, _],
         [_, _, I_br]] = I
        ret[I_tl] = matrix([[I_tl.update(l_ind="00")]])
        ret[o] = matrix([[one]])
        ret[I_br] = matrix([[one, T(Zero)],
                            [Zero, I_br.update(l_ind="33")]])
        return ret

class Fuse_I_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, I):
        ret = {}
        [[I_tl, _, _],
         [_, o, _],
         [_, _, I_br]] = I
        ret[I_tl] = matrix([[I_tl.update(l_ind="00"), Zero],
                            [T(Zero), one]])
        ret[o] = matrix([[one]])
        ret[I_br] = matrix([[I_br.update(l_ind="33")]])
        return ret

class Part_J_3x3 (TensorPartRule):
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, J):
        return \
          [[J.update(l_ind="tl"), Zero, ZERO],
           [T(J.update(l_ind="ml", rank=J.rank - 1)), Zero, T(Zero)],
           [ZERO, J.update(l_ind="bm", rank=J.rank - 1), J.update(l_ind="br")]]

class Repart_J_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, J):
        ret = {}
        [[J_tl, _, _],
         [Tj_ml, _, _],
         [_, j_bm, J_br]] = J
        ret[J_tl] = matrix([[J_tl.update(l_ind="00")]])
        ret[Tj_ml] = matrix([[Tj_ml.update(l_ind="10")]])
        ret[j_bm] = matrix([[one],
                            [Zero]])
        ret[J_br] = matrix([[zero, T(Zero)],
                            [j_bm.update(l_ind="32"), J_br.update(l_ind="33")]])
        return ret

class Fuse_J_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, J):
        ret = {}
        [[J_tl, _, _],
         [Tj_ml, _, _],
         [_, j_bm, J_br]] = J
        print "Fuse_J_3x3: Tj_ml", Tj_ml
        ret[J_tl] = matrix([[J_tl.update(l_ind="00"), Zero],
                            [Tj_ml.update(l_ind="10"), zero]])
        ret[Tj_ml] = matrix([T(Zero), one])
        # FIXME: Bug with Fuse printing layout should be
        ret[j_bm] = matrix([[j_bm.update(l_ind="32")]])
        ret[J_br] = matrix([[J_br.update(l_ind="33")]])
        return ret

class Part_I_J_3x3 (TensorPartRule):
    """Partition Rule for I - J"""
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, I_J):
        return \
          [[I_J.update(l_ind="tl"), Zero, Zero],
           [-T(I_J.update(l_ind="ml", rank=I_J.rank - 1)), one, T(Zero)],
           [ZERO, I_J.update(l_ind="bm",rank=I_J.rank - 1), I_J.update(l_ind="br")]]

class Repart_I_J_3x3 (TensorRepartFuseRule):
    """Special Repartition rule for I - J"""
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, I_J):
        ret = {}
        [[I_J_tl, _, _],
         [T_m_e_ml, one_mm, _],
         [_, e_bm, I_J_br]] = I_J
        e_ml = T_m_e_ml.args[1].args[0] # Unpack e_ml from -T(e_ml)
        ret[I_J_tl] = matrix([[I_J_tl.update(l_ind="00")]])
        ret[T_m_e_ml] = matrix([[-T(e_ml).update(l_ind="10")]])
        ret[one_mm] = matrix([[one_mm]])
        ret[e_bm] = matrix([[-one, one],
                                 [zero, e_bm.update(l_ind="32")]])
        ret[I_J_br] = matrix([[T(Zero)],
                                  [I_J_br.update(l_ind="33")]])
        return ret

class Fuse_I_J_3x3 (TensorRepartFuseRule):
    """Special Fuse rule for I - J"""
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, I_J):
        ret = {}
        [[I_J_tl, _, _],
         [T_m_e_ml, one_mm, _],
         [_, e_bm, I_J_br]] = I_J
        e_ml = T_m_e_ml.args[1].args[0] # Unpack e_ml from -T(e_ml)
        ret[I_J_tl] = matrix([[I_J_tl.update(l_ind="00"), Zero],
                                   [-T(e_ml.update(l_ind="10")), one_mm]])
        ret[T_m_e_ml] = matrix([[T(Zero), -one]])
        ret[one_mm] = matrix([[one_mm]])
        ret[e_bm] = matrix([[e_bm.update(l_ind="32")]])
        ret[I_J_br] = matrix([[I_J_br.update(l_ind="33")]])
        return ret


class Part_I_U_3x3 (TensorPartRule):
    """Partition Rule for I + U"""
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, I_U):
        return \
          [[I_U.update(l_ind="tl"), I_U.update(l_ind="tm", rank=1), I_U.update(l_ind="tr")],
           [T(Zero), one, T(I_U.update(l_ind="mm", rank=1))],
           [ZERO, Zero, I_U.update(l_ind="br")]]

class Repart_I_U_3x3 (TensorRepartFuseRule):
    """Special Repartition rule for I + U"""
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, I_U):
        ret = {}
        [[I_U_tl, u_tm, U_tr],
         [_, i_u_mm, t_u_mr],
         [_, _, I_U_br]] = I_U
        u_mr = t_u_mr.args[0]
        ret[I_U_tl] = matrix([[I_U_tl.update(l_ind="00")]])
        ret[u_tm] = matrix([[u_tm.update(l_ind="01")]])
        ret[U_tr] = matrix([[U_tr.update(l_ind="02", rank=1), U_tr.update(l_ind="03")]])
        ret[i_u_mm] = matrix([[one]])
        ret[t_u_mr] = matrix([[u_mr.update(l_ind="12", rank=0), T(u_mr.update(l_ind="13"))]])
        ret[I_U_br] = matrix([[one, T(I_U_br.update(l_ind="23", rank=1))],
                                   [Zero, I_U_br.update(l_ind="33")]])
        return ret

class Fuse_I_U_3x3 (TensorRepartFuseRule):
    """Special Fuse rule for I + U"""
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, I_U):
        ret = {}
        [[I_U_tl, u_tm, U_tr],
         [_, i_u_mm, t_u_mr],
         [_, _, I_U_br]] = I_U
        ret[I_U_tl] = matrix([[I_U_tl.update(l_ind="00"), I_U_tl.update(l_ind="01", rank=1)],
                              [T(Zero), one]])
        ret[u_tm] = matrix([[u_tm.update(l_ind="01")],
                            [u_tm.update(l_ind="12", rank=0)]])
        ret[U_tr] = matrix([[U_tr.update(l_ind="03")],
                            [U_tr.update(l_ind="13", rank=1)]])
        ret[i_u_mm] = matrix([[one]])
        ret[t_u_mr] = matrix([[t_u_mr.update(l_ind="23")]])
        ret[I_U_br] = matrix([[I_U_br.update(l_ind="33")]])
        return ret


class Part_H_3x3 (TensorPartRule):
    shape = (3, 3)
    _latex_head = "\FLAThreeByThree"
    def __call__(self, H):
        return \
          [[H.update(l_ind="tl"), H.update(l_ind="tm", rank=1), H.update(l_ind="tr")],
           [T(H.update(l_ind="ml", rank=1)), H.update(l_ind="mm", rank=0), T(H.update(l_ind="mr", rank=1))],
           [ZERO, H.update(l_ind="bm", rank=1), H.update(l_ind="br")]]

class Repart_H_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, H):
        ret = {}
        [[H_tl, h_tm, H_tr],
         [Th_ml, eta_mm, Th_mr],
         [_, h_bm, H_br]] = H
        ret[H_tl] = matrix([[H_tl.update(l_ind="00")]])
        ret[h_tm] = matrix([[h_tm.update(l_ind="01")]])
        ret[H_tr] = matrix([[h_tm.update(l_ind="02"), H_tl.update(l_ind="00")]])

        ret[Th_ml] = matrix([[Th_ml.update(l_ind="10")]])
        ret[eta_mm] = matrix([[eta_mm.update(l_ind="11")]])
        ret[Th_mr] = matrix([[eta_mm.update(l_ind="12"), Th_mr.update(l_ind="13")]])

        ret[h_bm] = matrix([[eta_mm.update(l_ind="21")],
                            [Zero]])
        ret[H_br] = matrix([[eta_mm.update(l_ind="22"), Th_mr.update(l_ind="23")],
                            [h_bm.update(l_ind="32"), H_br.update(l_ind="33")]])
        return ret

class Fuse_H_3x3 (TensorRepartFuseRule):
    shape = (3, 3)
    reshape = (4, 4)
    _latex_head = "\FLAFourByFour"
    def __call__(self, H):
        ret = {}
        [[H_tl, h_tm, H_tr],
         [Th_ml, eta_mm, Th_mr],
         [_, h_bm, H_br]] = H
        ret[H_tl] = matrix([[H_tl.update(l_ind="00"), h_tm.update(l_ind="01")],
                            [Th_ml.update(l_ind="10"), eta_mm.update(l_ind="11")]])
        ret[h_tm] = matrix([[h_tm.update(l_ind="02")],
                            [eta_mm.update(l_ind="12")]])
        ret[H_tr] = matrix([[H_tr.update(l_ind="03")],
                            [Th_mr.update(l_ind="13")]])

        ret[Th_ml] = matrix([[T(Zero), eta_mm.update(l_ind="21")]])
        ret[eta_mm] = matrix([[eta_mm.update(l_ind="22")]])
        ret[Th_mr] = matrix([[Th_mr.update(l_ind="23")]])

        ret[h_bm] = matrix([[h_bm.update(l_ind="32")]])
        ret[H_br] = matrix([[H_br.update(l_ind="33")]])
        return ret
