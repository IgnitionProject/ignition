"""General generators for SFL language"""

import os
import sys

from .proteus_coefficient_printer import ProteusCoefficientPrinter


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
    def to_file(self, filename=None):
        printer = ProteusCoefficientPrinter(self)
        # FIXME: Hack for filenames
        if filename is None:
            filename = os.path.split(sys.argv[0])[1][:-3]+"_proteus.py"
        with open(filename, 'w') as f:
            f.write(printer.print_file())

    def to_coefficient_class(self):
        self.to_file()


class UFLGenerator(SFLGenerator):
    """SFL generator for UFL language

    """
    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate())


def generate(framework, expr, **kwargs):
    """Generates the equation in a lower level framework"""
    if framework == "proteus":
        return ProteusCoefficientGenerator(expr, **kwargs).to_coefficient_class()

