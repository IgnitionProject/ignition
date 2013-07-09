"""Generator for Proteus coefficient evaluator"""

from ...utils.code_tools import indent_code

coefficient_header = """
/* Proteus Coefficient file generated from Ignition */
"""


class ProteusCoefficientPrinter(SFLPrinter):
    """Generator for Proteus Coefficient evaluator"""

     def __init__(self, generator):
        self._generator = generator

    @staticmethod
    def _print_header(indent):
        return indent_code(coefficient_header, indent)

    def _print_independent_evals(self, indent):
        expr = self._generate.get_independent_evals()


    def print_file(self, indent=0):
        ret_code = ""
        ret_code += self._print_header(indent)
        return ret_code
