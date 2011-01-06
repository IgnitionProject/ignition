"""Code generator for PME Language"""

from ignition.flame.pobj import PObj
from ignition.utils import flatten
from ignition.flame.tensors.solvers import all_back_sub
from ignition.flame.printing import get_printer

class PAlgGenerator (object):
    """Wrapper object for generating partitioned algorithms.

    operation: The operation to generate
    args: List of PObjs that are input for the operation.
    """

    def __init__ (self, loop_inv_op, *args, **kws):
        self.loop_inv_op = loop_inv_op
        self._args = args
        self.op = kws.get("op", None)
        if self.op:
            self.op_applied = self.op(*map(lambda x: x.obj, args))
        else:
            self.op_applied = None
        self.inputs = filter(lambda x: x.arg_src in \
                             [PObj.ARG_SRC.Input, PObj.ARG_SRC.Overwrite],
                             args)
        self.outputs = filter(lambda x: x.arg_src in \
                             [PObj.ARG_SRC.Output, PObj.ARG_SRC.Overwrite],
                             args)
        self.out_only = filter(lambda x: x.arg_src == PObj.ARG_SRC.Output,
                               args)
        self.operands = self.inputs + self.out_only
        if len(self.outputs) == 0:
            raise ValueError, \
             "PAlgGenerator requires at least one output, none given."
        self.debug = False
        self.updater = kws.get("updater", None)

    @property
    def partition (self):
        """Partition mapping"""
        ret_dict = {}
        for v in self._args:
            ret_dict[v.obj] = v.part
        return ret_dict

    @property
    def repartition (self):
        """Repartition mapping"""
        ret_dict = {}
        for v in self._args:
            ret_dict[v.obj] = v.repart
        return ret_dict

    @property
    def fuse (self):
        """Fuse mapping"""
        ret_dict = {}
        for v in self._args:
            ret_dict[v.obj] = v.fuse
        return ret_dict

    def _repart_invariant(self):
        return self.loop_inv_op(*map(lambda o: o.repart, self._args))

    def _fuse_invariant(self):
        return self.loop_inv_op(*map(lambda o: o.fuse, self._args))

    def _loop_invariant(self):
        return self.loop_inv_op(*map(lambda o: o.part, self._args))

    def _guard(self):
        return map(lambda o:o.part[-1], self.outputs)

    def gen_update (self, filename=None, type=None):
        """Generates the loop updates and pre/post conditions inside loop."""
        self.loop_inv = self._loop_invariant()
        self.b4_eqns = self._repart_invariant()
        self.aft_eqns = self._fuse_invariant()
        self.guard = self._guard()
        self.update_tups = self.updater(self.b4_eqns, self.aft_eqns)
        if len(self.update_tups) == 0:
            print "PAlgGenerator.generate: no updates found."
            self.update = None
        else:
            self.update = self.update_tups[0][0]

def generate (filename=None, filetype=None, op=None, loop_inv=None, inv_args=[],
              PME=None, updater=None):
    """Utility function for generating a flame algorithm.
    
    Will create a generator object and write it to file, then return the
    generator object.
    
    For more complete documentation see the PAlgGenerator object and 
    the printing module.
    """
    gen_obj = PAlgGenerator(loop_inv, *inv_args, op=op, updater=updater)
    gen_obj.gen_update(filename, filetype)
    get_printer(gen_obj, filename, filetype).write()
    return gen_obj

def tensor_updater (b4_eqns, aft_eqns, levels= -1, num_sols=1):
    """Updater calling tensor solvers."""
    knowns = flatten([eqn.atoms() for eqn in b4_eqns])
    print knowns
    sol_dicts = all_back_sub(aft_eqns, knowns, levels)
    sol_dicts = sol_dicts[:num_sols]
    return sol_dicts

