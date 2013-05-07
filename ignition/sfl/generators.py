"""General generators for SFL language"""

import os
import sys

from proteus_script_printer import ProteusScriptPrinter

class SFLGenerator(object):
    """Base class for strong form language generator.

    """
    def __init__(self, expr):
        self.expr = expr

    def generate(self):
        pass

class ProteusGenerator(SFLGenerator):
    """SFL generator for proteus framework

    """
    def to_file(self, filename=None):
        printer = ProteusScriptPrinter(self)
        # FIXME: Hack for filenames
        if filename is None:
            filename = os.path.split(sys.argv[0])[1][:-3]+"_proteus.py"
        with open(filename, 'w') as f:
            f.write(printer.print_file())

class UFLGenerator(SFLGenerator):
    """SFL generator for UFL language

    """
    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate())


def generate(framework, expr):
    """Generates the equation in a lower level framework"""
    if framework == "proteus":
        return ProteusGenerator(expr)
    
