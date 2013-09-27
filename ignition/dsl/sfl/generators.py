"""General generators for SFL language"""

import os
import sys

from .proteus_coefficient_printer import ProteusCoefficientPrinter
from ...code_tools import code_obj

class SFLGenerator(object):
    """Base class for strong form language generator.

    """
    def __init__(self, expr, **kwargs):
        self.expr = expr
        self.kwargs = kwargs

    def generate(self):
        pass


class ProteusCoefficientGenerator(SFLGenerator):
    """SFL generator for proteus coefficient evaluation

    """

    def __init__(self, expr, **kwargs):
        super(ProteusCoefficientGenerator, self).__init__(expr, **kwargs)
        self._filename = None
        self._classname = None
        self.class_dag = None

    @property
    def filename(self):
        if self._filename is None:
            # Try to get filename from keywords
            if "filename" in self.kwargs:
                self._filename = self.kwargs["filename"]
            else:
                # Get filename from script name
                self._filename = os.path.split(sys.argv[0])[1][:-3]+"_proteus.py"
        return self._filename

    @property
    def classname(self):
        if self._classname is None:
            # Try to get class name from keywords
            if "classname" in self.kwargs:
                self._classname = self.kwargs["classname"]
            else:
                # Set class name from script name
                self._classname = os.path.split(sys.argv[0])[1][:-3]\
                    .title().replace("_", "") \
                    + "Coefficients"
            return self._classname

    def gen_init_func_node(self):
        # XXX: Much hardcoded here.
        nc = code_obj.Variable("nc", int, var_init=1)
        _M, _A, _B, _C = map(lambda x: code_obj.Variable(x, int, var_init=0),
                             ["M", "A", "B", "C"])
        _rFunc = code_obj.Variable("rFunc", "function", var_init=None)
        useSparseDiffusion = code_obj.Variable("useSparseDiffusion",
                                                bool, var_init=True)
        default_input_vars = [_M, _A, _B, _C, _rFunc, useSparseDiffusion]
        args = [nc] + default_input_vars
        constructor = self.class_dag.create_constructor(args)

        member_names = ["M", "A", "B", "C"],
        M, A, B, C = map(lambda x, v: code_obj.Variable(x, int, var_init=v),
                          zip(member_names, default_input_vars))
        rFunc = code_obj.Variable('rFunc', "function", _rFunc)

        member_vars = [M, A, B, C, rFunc]
        map(lambda x: self.class_dag.add_member_variable(x), member_vars)
        tmp_names = ["mass", "advection", "diffusion", "potential", "reaction",
                     "hamiltonian"]
        mass, advection, diffusion, potential, reaction, hamiltonian = \
            map(lambda name: code_obj.IndexedVariable(name, var_init="{}"),
                tmp_names)
        tmp_vars = [mass, advection, diffusion, potential, reaction,
                    hamiltonian]
        map(lambda x: constructor.add_object(x), member_vars + tmp_vars)

        init_loop = code_obj.LoopNode('for', nc)
        init_loop.add_statement("=", mass.index_stmt(init_loop.idx),
                                "{%s, 'linear'}" % init_loop.idx)
        init_loop.add_statement("=", advection.index_stmt(init_loop.idx),
                                "{%s, 'linear'}" % init_loop.idx)
        init_loop.add_statement("=", diffusion.index_stmt(init_loop.idx),
                                "{%s, {%s, 'constant'}}" %
                                (init_loop.idx, init_loop.idx))
        init_loop.add_statement("=", potential.index_stmt(init_loop.idx),
                                "{%s, 'u'}" % init_loop.idx)
        init_loop.add_statement("=", reaction.index_stmt(init_loop.idx),
                                "{%s, 'linear'}" % init_loop.idx)

        init_args = ", ".join(tmp_names +
                              ["useSparseDiffusion = useSparseDiffusion"])
        init_loop.add_statement("%(parent)s.__init__(self, %(args)s))" %
                                {"parent": self.class_dag.parents[0],
                                 "args": init_args,
                                 })

    def gen_coefficient_class(self, classname=None):
        if classname is not None:
            self._classname = classname
        self.class_dag = code_obj.ClassNode(self.classname,
                                             parents=["TC_Base"])
        self.gen_init_func_node()

    def to_file(self, filename=None):
        self.gen_coefficient_class()
        printer = ProteusCoefficientPrinter(self)
        if filename is not None:
            self._filename = filename
        with open(self.filename, 'w') as f:
            print("Writing proteus coefficient file to %s" % self.filename)
            f.write(printer.print_file())


class UFLGenerator(SFLGenerator):
    """SFL generator for UFL language"""
    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate())


def generate(framework, expr, **kwargs):
    """Generates the equation in a lower level framework"""
    if framework == "proteus":
        return ProteusCoefficientGenerator(expr, **kwargs).to_file()
