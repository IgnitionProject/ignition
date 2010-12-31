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

    def generate (self, filename=None, type=None):
        self.loop_inv = "" #self.op(*self._args)
        self.b4_eqns = self.repart_invariant()
        self.aft_eqns = self.fuse_invariant()
#        print self.b4_eqns
#        print self.aft_eqns
        self.update_tups = self.updater(self.b4_eqns, self.aft_eqns)
#        if self.update_tups:
#            print "PAlgGenerator.generate: update_eqns"
#            for up_dict, _ in self.update_tups:
#                for var, update in up_dict.iteritems():
#                    print "  ", var, " = ", update
        if len(self.update_tups) == 0:
            print "PAlgGenerator.generate: no updates found."
            return
        self.update = self.update_tups[0][0]

def generate (filename=None, filetype=None, loop_inv=None, inv_args=[],
              PME=None, updater=None):
    """Utility function for generating a flame algorithm.
    
    Will create a generator object and write it to file, then return the
    generator object.
    
    For more complete documentation see the PAlgGenerator object and 
    the printing module.
    """
    gen_obj = PAlgGenerator(loop_inv, *inv_args, updater=updater)
    gen_obj.generate(filename, filetype)
    get_printer(gen_obj, filename, filetype).write()
    return gen_obj

def tensor_updater (b4_eqns, aft_eqns, levels= -1, num_sols=1):
    """Updater calling tensor solvers."""
    knowns = flatten([eqn.atoms() for eqn in b4_eqns])
    print knowns
    sol_dicts = all_back_sub(aft_eqns, knowns, levels)
    sol_dicts = sol_dicts[:num_sols]
    return sol_dicts

