1"""Code printers from abstract code graph"""

class CodePrinter(object):
    """Base class for language based code printers"""
    pass


class CBlockPrinter(CodePrinter):
    def __init__(self):
        super(CodePrinter, self).__init__()
        self.variables = {}
        self.code_str = ""

    def add_for_loop(self, start=0, stop=None, inc=1, loop_idx=None, indent=0):
        """Adds a c-code snippet to a loop"""
        ret_str = "for (%(loop_idx_type)s %(loop_idx)s = %(start)s; " \
                  "%(loop_idx)s < %(stop)s; %(loop_idx)s += %(inc)s) {\n"
        ret_str += indent_code(code_str, indent + 4)
        return ret_str


class CFunctionPrinter(CBlockPrinter):
    pass


class CFilePrinter(CodePrinter):
    """Code printer for C language"""

    def __init__(self):
        self.blocks = []

