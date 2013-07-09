"""Module for code to represent code objects and DAGs"""

from ..utils.iterators import counting_iter

VAR_COUNTER = counting_iter()

class CodeObj(object):
    """Base node class for Code DAG"""

    name = "codeobj"
    LOOP_IDX_PREFIX = "idx"

    def __init__(self):
        super(CodeObj, self).__init__()
        self.objs = []
        self.idx_vars = []

    def add_function(self, name, **kws):
        node = FunctionNode(name, **kws)
        self.objs.append(node)
        return node

    def add_for_loop(self, **kws):
        node = LoopNode('for', **kws)
        self.objs.append(node)
        return self

    def add_statement(self, *args, **kws):
        self.objs.append(Statement(*args, **kws))
        return self

    def add_object(self, code_obj):
        self.objs.append(code_obj)
        return self

    def next_idx_var(self, idx_type="int"):
        """Returns a free index to use in code"""
        idx_name = self.LOOP_IDX_PREFIX + "_" + str(VAR_COUNTER.next())
        next_idx = Variable(idx_name, idx_type)
        self.idx_vars.append(next_idx)
        return next_idx

    def get_functions(self):
        return map(lambda y: y.func_name, filter(lambda x: isinstance(x, FunctionNode), self.objs))

    def get_vars(self):
        vars = filter(lambda x: isinstance(x, Variable), self.objs)
        loops = filter(lambda x: isinstance(x, LoopNode) and x.kind == "for", self.objs)
        for loop in loops:
            if not loop.idx.declared:
                vars.append(loop.idx)
        return vars


class Statement(CodeObj):

    name = "statement"

    def __init__(self, operator, *args, **kws):
        super(Statement, self).__init__()
        self.operator = operator
        self.args = args

    def __str__(self):
        operator = self.operator
        args = self.args
        if len(args) == 1:
            ret_str =  str(operator) + " " + str(args[0])
        elif len(args) == 2:
            ret_str = " ".join([str(args[0]), str(operator), str(args[1])])
        else:
            ret_str = " ".join(["<Statement: %s, %s>", str(operator), " ".join(args)])
        return ret_str


class Variable(CodeObj):
    """Represents a variable"""

    name = "variable"

    def __init__(self, var_name, var_type, **kws):
        super(Variable, self).__init__()
        self.generated = False
        self.declared = False
        self.var_name = var_name
        self.var_type = var_type
        self.init_var = kws.get("init_var", None)

    def __str__(self):
        return self.var_name

    def __add__(self, other):
        return Statement('+', self, other)


class IndexedVariable(Variable):
    """Represents a variable that can be indexed"""

    name = "indexed_variable"

    def __init__(self, var_name, var_type, shape=None, **kws):
        super(IndexedVariable, self).__init__(var_name, var_type, **kws)
        self.shape = shape

    def index_stmt(self, idx):
        """Returns a statement for indexing"""
        return Statement("index", self, idx)


class BlockNode(CodeObj):
    """Represents a code block for printing"""

    name = 'blocknode'


class LoopNode(BlockNode):

    name = "loopnode"

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

    name = "functionnode"

    def __init__(self, func_name, ret_type=None, inputs=None, output=None):
        super(FunctionNode, self).__init__()
        self.func_name = func_name
        self.ret_type = ret_type
        if ret_type is None and output is not None and output.var_type is not None:
            self.ret_type = output.var_type
        self.inputs = [] if inputs is None else inputs
        self.output = output

    def add_function(self, name, **kws):
        raise RuntimeError("Nested functions not currently supported")

    def add_return(self, variable):
        self.outputs.append(variable)
