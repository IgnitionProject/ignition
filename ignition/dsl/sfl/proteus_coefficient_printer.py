"""Generator for Proteus coefficient evaluator"""

from .sfl_printer import SFLPrinter
from ...code_tools import comment_code, indent_code


coefficient_header = """\
Proteus Coefficient file generated from Ignition
"""

class_header = """\
class %{class_name}s(TC_base):
"""


class ProteusCoefficientPrinter(SFLPrinter):
    """Generator for Proteus Coefficient evaluator"""

    language = 'Python'
    comment_str = '//'
    block_comment_tuple = ('"""', '"""')

    def _print_header(self, indent):
        return comment_code(indent_code(coefficient_header, indent),
                            block_comment=self.block_comment_tuple)

    def _print_class_head(self, generate, indent=0):
        ret_str = class_header(generate.classname)


    def _print_independent_evals(self, indent=0):
        expr = self._generate.get_independent_evals()
        return indent_code(expr, indent)

    def print_file(self, indent=0):
        ret_code = ""
        ret_code += self._print_header(indent)
        return ret_code
