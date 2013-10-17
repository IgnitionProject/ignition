"""Generator for Proteus coefficient evaluator"""

from .sfl_printer import SFLPrinter
from ...code_tools import comment_code, indent_code, PythonCodePrinter


coefficient_header = """\
Proteus Coefficient file generated from Ignition
"""


class ProteusCoefficientPrinter(SFLPrinter):
    """Generator for Proteus Coefficient evaluator"""

    language = 'Python'
    comment_str = '//'
    block_comment_tuple = ('"""', '"""\n')

    def __init__(self, generator):
        super(ProteusCoefficientPrinter, self).__init__(generator)
        self._printer = PythonCodePrinter(self._generator.class_dag,
                                          self._generator.modules)

    def _print_header(self, indent):
        return comment_code(indent_code(coefficient_header, indent),
                            block_comment=self.block_comment_tuple)

    def print_file(self, filename, indent=0):
        self._printer.to_file(filename, top_comment=coefficient_header)
