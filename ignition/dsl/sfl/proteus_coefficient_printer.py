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

    def _print_header(self, indent):
        return comment_code(indent_code(coefficient_header, indent),
                            block_comment=self.block_comment_tuple)

    def print_file(self, indent=0):
        ret_code = ""
        ret_code += self._print_header(indent)
        ret_code += PythonCodePrinter(self._generator.class_dag).code_str()
        return ret_code
