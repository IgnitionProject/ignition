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
        args = [code_obj.Variable("nc", int, var_init=1)]
        args += map(lambda x: code_obj.Variable(x, int, var_init=0),
                    ["M", "A", "B", "C"])
        node = code_obj.FunctionNode("__init__", args)
        # FIXME: Need to generate rest of init func.x
        return node

    def gen_coefficient_class(self, classname=None):
        if classname is not None:
            self._classname = classname
        self.class_dag = code_obj.ClassNode(self.classname)
        self.class_dag.add_init_func(self.gen_init_func_node())

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

