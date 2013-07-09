from numpy import matrix, zeros

from ...utils import Enum

class DenseRepart (object):
    """Defines repartitioning rules"""

    DIRS = Enum(("BOTRIGHT", "BR"), ("TOPLEFT", "TL"), ("TOPRIGHT", "TR"),
                ("BOTLEFT", "BL"), "BOTTOM", "TOP", "LEFT", "RIGHT", "NoPart")

    OPPDIR = {DIRS.BOTRIGHT : DIRS.TOPLEFT,
              DIRS.BOTLEFT : DIRS.TOPRIGHT,
              DIRS.TOPLEFT : DIRS.BOTRIGHT,
              DIRS.TOPRIGHT : DIRS.BOTLEFT,
              DIRS.BOTTOM : DIRS.TOP,
              DIRS.TOP : DIRS.BOTTOM,
              DIRS.LEFT : DIRS.RIGHT,
              DIRS.RIGHT : DIRS.LEFT,
              }

    def __init__ (self, repart, direction):
        assert type(repart) == list and len(repart) >= 1 and \
               type(repart[0]) == list, "Repart arg in wrong state."
        self.shape = (len(repart), len(repart[0]))
        self._direc = direction
        self._repart = repart

    def __iter__ (self):
        for i in self._repart:
            yield i

    def tolist (self):
        """Returns a list of the repartion entries in row major order"""
        def _resize(M, N):
            """Unroll repartition obj from shape (I,J) to (M,N)"""
            ret = zeros((M, N), dtype=object)
            xr = 0 # extra rows
            for m in xrange(self.shape[0]):
                xc = 0 # extra columns
                for n in xrange(self.shape[1]):
                    mat = self._repart[m][n]
                    r, c = mat.shape
                    for i in xrange(r):
                        for j in xrange(c):
                            ret[m + xr + i][n + xc + j] = mat[i, j]
                    xc += c - 1 # Add extra column to be added to next column
                xr += r - 1 # Add extra rows to be added to next row                
            return ret

        if self._direc in [self.DIRS.TOPLEFT, self.DIRS.BOTRIGHT]:
            return flatten(_resize(self.shape[0] + 1, self.shape[1] + 1))
        elif self._direc in [self.DIRS.TOP, self.DIRS.BOTTOM]:
            return flatten(_resize(self.shape[0] + 1, self.shape[1]))
        elif self._direc in [self.DIRS.LEFT, self.DIRS.RIGHT]:
            return flatten(_resize(self.shape[0], self.shape[1]))
        else:
            raise NotImplementedError, "DenseRepart.tolist not implemented "\
                                       "for direction %s" % (str(self._direc))


    @staticmethod
    def repart (P, direction=None, *args, **kws):
        assert isinstance(P, Partition), "Partition object in wrong state."
        size = "%dx%d" % (len(P.part), len(P.part[0]))
        fun_name = "repart" + size
        if not hasattr(DenseRepart, fun_name):
            raise AttributeError, "Unable to repartition size %s" % size
        rp = getattr(DenseRepart, fun_name)(P, direction, * args, **kws)
        return DenseRepart(apply_rules(P.part, rp), direction)

    @staticmethod
    def _checksize (P, o, i):
        return type(P.part) == list and len(P.part) == o \
               and type(P.part[0]) == list and len(P.part[0]) == i

    @staticmethod
    def repart2x2 (P, direction=None, *args, **kws):
        """DenseRepart rules for a 2x2 array into a 3x3 version"""
        assert DenseRepart._checksize(P, 2, 2), "P must be 2X2."
        ret_dict = {}
        [[Ptl, Ptr], [Pbl, Pbr]] = P
        if direction in [DenseRepart.DIRS.BOTRIGHT, None]:
            ret_dict[Ptl] = matrix(Ptl.new_ind("00"))
            ret_dict[Ptr] = matrix([Ptr.new_ind("01"),
                                    Ptr.new_ind("02")]) if Ptr.structure != Matrix.STRUCT.LT \
                            else matrix([Matrix('0'), Matrix('0')])
            ret_dict[Pbl] = matrix([[Pbl.new_ind("10")],
                             [Pbl.new_ind("20")]])
            ret_dict[Pbr] = matrix([[Pbr.new_ind("11"), Pbr.new_ind("12") if Pbr.structure != Matrix.STRUCT.LT \
                                    else Matrix('0')],
                             [Pbr.new_ind("21"), Pbr.new_ind("22")]])
        elif direction == DenseRepart.DIRS.TOPLEFT:
            ret_dict[Ptl] = matrix([[Ptl.new_ind("00"), Ptl.new_ind("01") if Ptl.structure != Matrix.STRUCT.LT \
                                    else Matrix('0')],
                             [Ptl.new_ind("10"), Ptl.new_ind("11")]])
            ret_dict[Ptr] = matrix([[Ptr.new_ind("02")],
                             [Ptr.new_ind("12")]]) if Ptr.structure != Matrix.STRUCT.LT \
                            else matrix([Matrix('0'), Matrix('0')])
            ret_dict[Pbl] = matrix([Pbl.new_ind("20"), Pbl.new_ind("21")])
            ret_dict[Pbr] = matrix(Pbr.new_ind("22"))
        else:
            raise ValueError, "Unknown direction.\n  given: %s" % direction
        return ret_dict


    @staticmethod
    def repart1x2 (P, direction=None, *args, **kws):
        """Repartion rule for a 1X2 array into a 1X3 array"""
        assert DenseRepart._checksize(P, 1, 2), "P must be 1X2."
        ret_dict = {}
        [[Pl, Pr]] = P
        if direction in [DenseRepart.DIRS.LEFT, None]:
            ret_dict[Pl] = matrix([Pl.new_ind("0"), Pl.new_ind("1")])
            ret_dict[Pr] = matrix(Pr.new_ind("2"))
        elif direction == DenseRepart.DIRS.RIGHT:
            ret_dict[Pl] = matrix(Pl.new_ind("0"))
            ret_dict[Pr] = matrix([Pr.new_ind("1"), Pr.new_ind("2")])
        else:
            raise ValueError, "Unknown direction.\n  given: %s" % direction
        return ret_dict


    @staticmethod
    def repart2x1 (P, direction=None, *args, **kws):
        """Repartion rule for a 2X1 array into a 3X1 array"""
        assert DenseRepart._checksize(P, 2, 1), "P must be 2X1."
        ret_dict = {}
        [[Pt], [Pb]] = P
        if direction in [DenseRepart.DIRS.BOTTOM, None]:
            ret_dict[Pt] = matrix(Pt.new_ind("0"))
            ret_dict[Pb] = matrix([[Pb.new_ind("1")], [Pb.new_ind("2")]])
        elif direction == DenseRepart.DIRS.TOP:
            ret_dict[Pt] = matrix([[Pt.new_ind("0")], [Pt.new_ind("1")]])
            ret_dict[Pb] = matrix(Pb.new_ind("2"))
        else:
            raise ValueError, "Unknown direction.\n  given: %s" % direction
        return ret_dict
