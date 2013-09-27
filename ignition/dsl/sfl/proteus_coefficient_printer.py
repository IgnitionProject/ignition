"""Generator for Proteus coefficient evaluator"""

from .sfl_printer import SFLPrinter
from ...code_tools import comment_code, indent_code, PythonCodePrinter


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

    def print_file(self, indent=0):
        ret_code = ""
        ret_code += self._print_header(indent)
        ret_code += PythonCodePrinter(self._generator.class_dag)
        return ret_code
