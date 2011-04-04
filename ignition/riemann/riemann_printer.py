"""Base classes for code printers"""

from ignition.utils import comment_code, indent_code

class RiemannPrinter (object):
    """Base class for Riemann printer objects"""
    comment_str = '//'

    def __init__ (self, generator):
        self._generator = generator

    def print_kernel_file (self, indent=0):
        return comment_code(self._generator.info(), self.comment_str) + \
               self._print_kernel_file(indent)

    @staticmethod
    def get_printer (generator):
        ret_obj = None
        language = generator.language
        evaluation = generator.evaluation
        if language == "pyclawpack":
            if evaluation == "pointwise":
                ret_obj = PyClawpackPrinter(generator)
            elif evaluation == "vectorized":
                ret_obj = VectorizedPyClawpackPrinter(generator)
        if ret_obj is None:
            raise NotImplementedError("No printer for generator.")
        return ret_obj

# Cyclic imports
from pyclawpack_printer import PyClawpackPrinter, VectorizedPyClawpackPrinter
