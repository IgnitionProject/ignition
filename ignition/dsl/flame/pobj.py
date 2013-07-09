"""Defines PME Language"""

from ...utils.enum import Enum


class PObj (object):
    """Represents a partitioned object

    The base for the PME language. Each object in a partitioned equation must
    derive from this class.

    Args:
        obj: The  underlying object being partitioned.

    Optional keyword arguments:
        size: 
            The size of the partition, currently a two-tuple. default: (2,2)

        dir: 
            The direction of the traversal, used for automatically selecting
            repart and fuse rules. Optional but default assumed if repart and 
            fuse rules are not given.
           
        props: 
            List of properties of partitioned object useful for choosing choosing
            partitition rules.  For example: ["Symmetric", "UpperTriangular",
            "LowerTriangular", "Input", "Output", "Overwritten"]
            
        part_fun: 
            Method for transforming object to list of objects.
            
        repart_fun: 
            Method that returns dictionary for partition to loop variables 
            before the loop updates.
            
        fuse_fun: 
            Method that returns dictionary for partition to loop variables
            after the loop updates.

    """

    ARG_SRC = Enum("Input", "Output", "Overwrite", "Computed")

    def __init__ (self, obj, *args, **kws):
        self.obj = obj
        self._args = args
        self._kws = kws
        self.size = kws.get("size", None)
        self.dir = kws.get("dir", None)
        self.part_fun = kws.get("part_fun", None)
        self._part = kws.get("part", None)
        self.part_subs = kws.get("part_subs", None)
        self.repart_fun = kws.get("repart_fun", None)
        self._repart = kws.get("repart", None)
        self.fuse_fun = kws.get("fuse_fun", None)
        self._fuse = kws.get("fuse", None)
        self.props = kws.get("props", [])
        self.arg_src = kws.get("arg_src", [])

    @property
    def part (self):
        if self._part is None:
            self._part = self.part_fun(self.obj)
        return self._part

    def _apply_partsub (self, subs):
        if self.part_subs is not None:
            return self.part_subs(self.part, subs)
        if type(self.part) is list:
            return self._apply_partsub_list(subs)
        raise NotImplementedError("Don't know how to substitute in obj of %s." \
                                  % type(self.part))

    def _apply_partsub_list (self, subs):
        def _recur(blst):
            if type(blst) is list:
                return map(_recur, blst)
            elif blst in subs:
                return subs[blst]
            else:
                return blst
        return _recur(self.part)

    @property
    def repart (self):
        """Returns the partition transformed by repart"""
        if self._repart is None:
            self._repart = self._apply_partsub(self.repart_fun(self.part))
        return self._repart

    @property
    def fuse (self):
        """Returns the partition transformed by fuse"""
        if self._fuse is None:
            self._fuse = self._apply_partsub(self.fuse_fun(self.part))
        return self._fuse

    def __iter__ (self):
        if self.part is None:
            raise NotImplementedError
        for p in self.part:
            yield p

    def __str__(self):
        return "PObj(%s)" % ",".join(self._args + ["%s = %s" % (k, v) for k, v in self._kws])

