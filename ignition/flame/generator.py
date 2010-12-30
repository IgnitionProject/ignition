"""Code generator for PME Language"""

from ignition.flame.pobj import PObj
from ignition.utils import flatten
from ignition.flame.tensors.solvers import all_back_sub

class PAlgGenerator (object):
    """Wrapper object for generating partitioned algorithms.

    operation: The operation to generate
    args: List of PObjs that are input for the operation.
    """

    def __init__ (self, operation, *args, **kws):
        self.op = operation
        self._args = args
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

    def repart_invariant(self):
        return self.op(*map(lambda o: o.repart, self._args))

    def fuse_invariant(self):
        return self.op(*map(lambda o: o.fuse, self._args))

    def generate (self, filename, type=None):
        b4_eqns = self.repart_invariant()
        aft_eqns = self.fuse_invariant()
        print b4_eqns
        print aft_eqns
#        update_dict = self.updater(b4_eqns, aft_eqns)
#        print "PAlgGenerator.generate: update_eqns"
#        for var, update in update_dict.iteritems():
#            print "  ", var, " = ", update

def generate (filename, loop_inv=None, inv_args=[], PME=None, updater=None):
    """Utility function for generating a flame algorithm
    
    For more complete documentation see the PAlgGenerator object.
    """
    return PAlgGenerator(loop_inv, *inv_args, updater=updater).generate(filename)


def tensor_updater (b4_eqns, aft_eqns, levels= -1, num_sols=1):
    """Updater calling tensor solvers."""
    knowns = flatten([eqn.atoms for eqn in b4_eqns])
    sol_dicts = all_back_sub(aft_eqns, knowns, levels)
    sol_dicts = sol_dicts[:num_sols]
    return sol_dicts

