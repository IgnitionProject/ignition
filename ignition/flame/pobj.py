"""Defines PME Language"""

import operator
from copy import deepcopy

from ignition.utils.enum import Enum


class PObj (object):
    """A partitioned object
    
    A partitioned object is the base for the PME language.  It has the 
    following attributes:
    
    name : The name of the object being partitioned.
    
    Optional keyword arguments

    Properties of the partition
    size: The size of the partition, currently a two-tuple. default: (2,2)
    dir:  The direction of the traversal, used for automatically selecting
          repart and fuse rules. Optional but default assumed if repart and 
          fuse rules are not given.
    props: List of properties of partitioned object useful for choosing choosing
           partitition rules.  For example: ["Symmetric", "UpperTriangular",
           "LowerTriangular", "Input", "Output", "Overwritten"]
          
    Methods for transforming object before and after loop updates
    part:   Method for transforming object to list of objects.
    repart: Method that returns dictionary for partition to loop variables 
            before the loop updates.
    fuse:   Method that returns dictionary for partition to loop variables
            after the loop updates.
            
    """

    ARG_SRC = Enum("Input", "Output", "Overwrite", "Computed")

    def __init__ (self, obj, *args, **kws):
        self.obj = obj
        self._args = args
        self._kws = kws
        self.size = kws.get("size", None)
        self.dir = kws.get("dir", None)
        self.part = kws.get("part", None)
        self.part_subs = kws.get("part_subs", None)
        self.repart = kws.get("repart", None)
        self.fuse = kws.get("fuse", None)
        self.props = kws.get("props", [])
        self.arg_src = kws.get("arg_src", [])

    def _apply_part_rule(self, rule):
        return self.part_subs(self.part, rule)

    def apply_repart (self):
        """Returns the partition object transformed by repart"""
        return _apply_part_rule(self.part)

    def apply_fuse (self):
        """Returns the partition object transformed by fuse"""
        return _apply_part_rule(self.fuse)

    def __iter__ (self):
        if self.part is None:
            raise NotImplementedError
        for p in self.part():
            yield p

    def __str__(self):
        return "PObj(%s)" % ",".join(self._args + ["%s = %s" % (k, v) for k, v in self._kws])

