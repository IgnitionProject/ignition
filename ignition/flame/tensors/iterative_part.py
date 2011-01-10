"""Partition rules for iterative methods"""

from numpy import matrix

from part import Fuse, Part, Repart
from basic_operators import T
from constants import one, Zero, zero

class Part_1x1 (Part):
    @staticmethod
    def __call__ (M):
        return [M]

class Repart_1x1 (Repart):
    @staticmethod
    def __call__ (M):
        return {M[0]:matrix(M)}

class Fuse_1x1 (Fuse):
    @staticmethod
    def __call__ (M):
        return {M[0]:matrix(M)}

class Part_1x3 (Part):
    @staticmethod
    def __call__ (M):
        return [M.update(l_ind="L"), M.update(l_ind="m", rank=M.rank - 1),
                M.update(l_ind="R")]

class Repart_1x3 (Repart):
    @staticmethod
    def __call__ (M):
        ret_dict = {}
        [M_l, m_m, M_r] = M
        ret_dict[M_l] = matrix([[M_l.update(l_ind="0")]])
        ret_dict[m_m] = matrix([[m_m.update(l_ind="1")]])
        ret_dict[M_r] = matrix([[M_r.update(l_ind="2", rank=1), M_r.update(l_ind="3")]])
        return ret_dict

class Fuse_1x3 (Fuse):
    @staticmethod
    def __call__ (M):
        ret_dict = {}
        [M_l, m_m, M_r] = M
        ret_dict[M_l] = matrix([M_l.update(l_ind="0"), m_m.update (l_ind="1")])
        ret_dict[m_m] = matrix([M_r.update(l_ind="2", rank=1)])
        ret_dict[M_r] = matrix([M_r.update(l_ind="3")])
        return ret_dict

class Part_J_3x3 (Part):
    @staticmethod
    def __call__(J):
        return \
          [[J.update(l_ind="tl"), Zero, Zero],
           [T(J.update(l_ind="ml", rank=J.rank - 1)), Zero, Zero],
           [Zero, J.update(l_ind="bm", rank=J.rank - 1), J.update(l_ind="br")]]

class Repart_J_3x3 (Repart):
    @staticmethod
    def __call__(J):
        ret_dict = {}
        [[J_tl, _, _],
         [Tj_ml, _, _],
         [_, j_bm, J_br]] = J
        ret_dict[J_tl] = matrix([[J_tl.update(l_ind="00")]])
        ret_dict[Tj_ml] = matrix([[Tj_ml.update(l_ind="10")]])
        ret_dict[j_bm] = matrix([[one, zero],
                                 [Zero, j_bm.update(l_ind="32")]])
        ret_dict[J_br] = matrix([[T(Zero)],
                                  [J_br.update(l_ind="33")]])
        return ret_dict

class Fuse_J_3x3 (Fuse):
    @staticmethod
    def __call__(J):
        ret_dict = {}
        [[J_tl, _, _],
         [Tj_ml, _, _],
         [_, j_bm, J_br]] = J
        ret_dict[J_tl] = matrix([[J_tl.update(l_ind="00"), Zero],
                                 [Tj_ml.update(l_ind="10"), zero]])
        ret_dict[Tj_ml] = matrix([T(Zero), one])
        ret_dict[j_bm] = matrix([j_bm.update(l_ind="32")])
        ret_dict[J_br] = matrix([J_br.update(l_ind="33")])
        return ret_dict
