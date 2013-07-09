from numpy import matrix, zeros

from ..prule import PartRule, RepartFuseRule
from ....utils import flatten_list

from printers import latex_print

class TensorPartRule(PartRule):

    _latex_head = "\Undefined"
    shape = (-1, -1)

    def _str (self, M):
        return str(M)

    def _latex (self, M):
        ret_str = self._latex_head
        for elem in M:
            if isinstance(elem, list):
                for e in elem:
                    ret_str += "{" + latex_print(e) + "}"
            else:
                ret_str += "{" + latex_print(elem) + "}"
        return ret_str

class TensorRepartFuseRule(RepartFuseRule):

    _latex_head = "\Undefined"
    shape = (-1, -1)
    reshape = (-1, -1)

    def _str (self, M):
        return str(self.tolist(M))

    def _latex (self, part):
        ret_str = self._latex_head
        for elem in flatten_list(self.tolist(part)):
            ret_str += "{" + latex_print(elem) + "}"
        return ret_str

    def tolist (self, part):
        """Returns a nested list of the repartion/fuse entries in row major order"""
        if self.shape == self.reshape:
            return part
        if self.shape[0] == self.shape[1] == 1:
            return self(part).tolist()
        elif self.shape[0] == 1:
            return self.tolist_row(part)
        elif self.shape[1] == 1:
            return self.tolist_column(part)
        else:
            return self.tolist_rank_2(part)

    def tolist_column(self, part):
        repart_obj = self(part)
        ret = zeros(self.reshape, dtype=object)
        xc = 0 # extra columns
        for n in xrange(self.shape[1]):
            mat = repart_obj.get(part[n], matrix([None]))
            _, c = mat.shape
            for j in xrange(c):
                ret[n + xc + j] = mat[0, j]
            xc += c - 1 # Add extra column to be added to next column            
        return ret.tolist()

    def tolist_row(self, part):
        repart_obj = self(part)
        ret = zeros(self.reshape, dtype=object)
        xr = 0 # extra columns
        for m in xrange(self.shape[0]):
            mat = repart_obj.get(part[m], matrix([None]))
            r, _ = mat.shape
            for i in xrange(r):
                ret[m + xr + i] = mat[i, 0]
            xr += r - 1 # Add extra column to be added to next column            
        return ret.tolist()

    def tolist_rank_2(self, part):
        repart_obj = self(part)
        ret = zeros(self.reshape, dtype=object)
        xr = 0 # extra rows
        for m in xrange(self.shape[0]):
            xc = 0 # extra columns
            for n in xrange(self.shape[1]):
                mat = repart_obj.get(part[m][n], matrix([[None]]))
                r, c = mat.shape
                for i in xrange(r):
                    for j in xrange(c):
                        ret[m + xr + i][n + xc + j] = mat[i, j]
                xc += c - 1 # Add extra column to be added to next column
            xr += r - 1 # Add extra rows to be added to next row                
        return ret.tolist()
