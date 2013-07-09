"""Code printers for UFL"""

from ...utils import indent_code
from .sfl_printer import SFLPrinter

class UFLPrinter(SFLPrinter):
    comment_str = "//"
    
    def _print_file(self, indent=0):
        return ""
