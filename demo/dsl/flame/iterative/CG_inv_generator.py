"""Demonstrates how to generate loop invariants from a single PME

In this example, we define the conjugent gradient PME and use it to generate
invariant operators.  These operators can then be passed to the flame generator
functions to generate worksheets or algorithms.
"""

from itertools import chain, combinations

import numpy as np

from ignition.dsl.flame import CONSTANTS, iterative_arg, PObj, T, TensorExpr

class InvariantGenerator( object ):
    """Abstract class for generating invariants from PME's.

    To use this class, subclass it and create an args tuple and PME.
    """

    def _get_tuple_args(self, obj):
        ret = obj
        if isinstance(obj, (PObj, list)):
            ret = []
            obj_list = list(obj)
            for item in obj_list:
                ret.append(self._get_tuple_args(item))
            ret = tuple(ret)
        elif isinstance(obj, TensorExpr):
            if obj in CONSTANTS:
                # We throw away constants since they don't need a new name
                ret = "_"
            else:
                ret = obj
        else:
            raise ValueError("Unable to handle obj %s of type %s" % \
                             (str(obj), type(obj)))
        return ret

    def _get_signature(self, fname):
        return "def %(fname)s(%(fargs)s):" % \
            {'fname': fname,
             'fargs': ", ".join(map(lambda o: str(self._get_tuple_args(o)),
                                    self.args)).replace("'", ""),
            }

    def _get_body(self, inv):
        return "    return " + str(inv)

    def __iter__(self):
        size = len(self.PME)
        for n, comb in enumerate(chain(*[combinations(range(size), i) \
                                         for i in xrange(1, size+1)])):
            invs =  [self.PME[idx] for idx in comb]
            code = self._get_signature(self.name+"_"+str(n))
            code += '\n'
            code += self._get_body( invs )
            yield code

class CGInvariantGenerator( InvariantGenerator ):
    A = iterative_arg("A", rank=2, part_suffix="1x1")
    X = iterative_arg("X", rank=2, part_suffix="1x3", arg_src="Overwrite")
    P = iterative_arg("P", rank=2, part_suffix="1x3", arg_src="Computed")
    I = iterative_arg("I", rank=2, part_suffix="I_3x3", arg_src="Computed")
    U = iterative_arg("U", rank=2, part_suffix="Upper_Bidiag_3x3", arg_src="Computed")
    J = iterative_arg("J", rank=2, part_suffix="J_3x3", arg_src="Computed")
    D = iterative_arg("D", rank=2, part_suffix="Diag_3x3", arg_src="Computed")
    R = iterative_arg("R", rank=2, part_suffix="1x3", arg_src="Computed")
    O = iterative_arg("O", rank=2, part_suffix="1x3", arg_src="Computed")

    args = [A, X, P, I, U, J, D, R, O]

    #Putting this here until I get PObjs combining better
    for arg in args:
        exec('%(name)s = np.matrix(%(name)s.part)' % {'name': arg.obj.name})

    PME = [X * (I + U) - P * D,
           A * P * D - R * (I - U),
           P * (I - J) - R,
           T(R) * R - O]

    name = 'cg_inv'


if __name__ == "__main__":
    with open("cg_inv.py", 'w') as fp:
        for code in CGInvariantGenerator():
            fp.write(code+"\n\n")

