
class Variable(object):

    def __init__(self, name, **kws):
        super(Variable, self).__init__()
        self.generated = False
        self.declared = False
        self.name = name


class CodeNode(object):
    """Base node class for Code DAG"""

    def __init__(self):
        super(CodeNode, self).__init__()
        self.children = []

class BlockNode(CodeNode):
    """Represents a code block for printing"""

    def __init__(self):
        super(BlockNode, self).__init__()

class FileNode(BlockNode):
    """Directed acyclic graph representing a 'file'"""
        pass

class FunctionNode(BlockNode):
    """Represents a function block"""

    def __init__(self, name, inputs=None, outputs=None):
        super(FunctionNode, self).__init__()
        self.name = name
        self.inputs = if inputs is None then [] else inputs
        self.outputs = if inputs is None then [] else inputs


class CodePrinter(object):
    """Base class for language based code printers"""
    LOOP_IDX_PREFIX = "idx"


class CBlockPrinter(CodePrinter):
    def __init__(self):
        super(CodePrinter, self).__init__()
        self.variables = {}
        self.code_str = ""

    def get_next_idx(self, idx_type="int"):
        """Returns a free index to use in code"""
        idx_vars = filter(lambda x: x.starts_with(self.LOOP_IDX_PREFIX),
                          self.variables.keys())
        next_idx = self.LOOP_IDX_PREFIX + "_" + len(idx_vars)
        self.variables[next_idx] = idx_type
        return next_idx

    def add_for_loop(self, code_str, start, stop, inc="1", loop_idx=None,
        loop_idx_type="int", indent=0):
        """Adds a c-code snippet to a loop"""
        ret_str = "for (%(loop_idx_type)s %(loop_idx)s = %(start)s; " \
                  "%(loop_idx)s < %(stop)s; %(loop_idx)s += %(inc)s) {\n"
        ret_str += indent_code(code_str, indent + 4)
        ret_str

class CFunctionPrinter(CBlockPrinter):


class CFilePrinter(CodePrinter):
    """Code printer for C language"""

    def __init__(self):
        self.blocks = []

