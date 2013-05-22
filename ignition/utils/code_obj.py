"""Module for code to represent code objects and DAGs"""

class CodeObj(object):
    """Top base class for ignition code representation"""
    pass


class Statement(CodeObj):
    def __init__(self, operator, *args):
        super(CodeObj, self).__init__()
        self.operator = operator
        self.args = args

    def __str__(self):
        operator = self.operator
        args = self.args
        if args == 1:
            return str(operator) + " " + str(args[0])
        elif args == 2:
            return " ".join([str(args[0]), str(operator), str(args[1])])
        else:
            return " ".join(["<Statement:", str(operator), " ".join(args)])


class Variable(CodeObj):
    """Represents a variable"""

    def __init__(self, name, var_type, **kws):
        super(Variable, self).__init__()
        self.generated = False
        self.declared = False
        self.name = name
        self.var_type = var_type

    def __str__(self):
        return name

    def __add__(self, other):
        return Statement('+', self, other)


class CodeNode(CodeObj):
    """Base node class for Code DAG"""
    LOOP_IDX_PREFIX = "idx"

    def __init__(self):
        super(CodeNode, self).__init__()
        self.objs = []
        self.idx_vars = []

    def add_function(self, name, inputs=None, outputs=None):
        node = FunctionNode(name, inputs, outputs)
        self.objs.append(node)
        return node

    def add_for_loop(self, start=0, stop=None, inc=1, idx=None):
        node = LoopNode('for', init=start, test=stop, idx=idx)
        self.objs.append(node)
        return node

    def add_statement(self, statement):
        self.objs.append(statement)
        return statement

    def next_idx_var(self, idx_type="int"):
        """Returns a free index to use in code"""
        next_idx = Variable(self.LOOP_IDX_PREFIX + "_" + str(len(self.idx_vars)), idx_type)
        self.idx_vars.append(idx_type)
        return next_idx


class BlockNode(CodeNode):
    """Represents a code block for printing"""

    def __init__(self):
        super(BlockNode, self).__init__()


class LoopNode(BlockNode):

    def __init__(self, kind, test=None, inc=None, init=None, idx=None):
        super(BlockNode, self).__init__()
        self.kind = kind
        self.test = test
        self.inc = inc
        self.init = init
        self.idx = idx if idx is not None else self.next_idx_var()

    def add_function(self, name, inputs=None, outputs=None):
        raise RuntimeError("Function blocks in loops not supported")


class FunctionNode(BlockNode):
    """Represents a function block"""

    def __init__(self, name, inputs=None, outputs=None):
        super(FunctionNode, self).__init__()
        self.name = name
        self.inputs = [] if inputs is None else inputs
        self.outputs = [] if inputs is None else inputs

    def add_function(self, name, inputs=None, outputs=None):
        raise RuntimeError("Nested functions not currently supported")

    def add_return(self, variable):
        self.outputs.append(variable)
