"""Module for code to represent code objects and DAGs"""

from collections import OrderedDict
import warnings

from ..utils.iterators import counting_iter
from ..utils.ordered_set import OrderedSet
from .code_tools import NIL


VAR_COUNTER = counting_iter()


class CodeObj(object):
    """Base node class for Code DAG"""

    name = "codeobj"
    LOOP_IDX_PREFIX = "idx"

    def __init__(self):
        super(CodeObj, self).__init__()
        self.objs = OrderedSet([])
        self.idx_vars = OrderedSet([])
        self.class_member = False

    def add_object(self, code_obj):
        self.objs.add(code_obj)
        return self

    def add_statement(self, *args, **kws):
        self.objs.add(Statement(*args, **kws))
        return self

    def next_idx_var(self, idx_type="int"):
        """Returns a free index to use in code"""
        idx_name = self.LOOP_IDX_PREFIX + "_" + str(VAR_COUNTER.next())
        next_idx = Variable(idx_name, idx_type)
        self.idx_vars.add(next_idx)
        return next_idx

    @property
    def expressions(self):
        return filter(lambda y: isinstance(y, Expression), self.objs)

    @property
    def functions(self):
        return filter(lambda x: isinstance(x, FunctionNode), self.objs)

    @property
    def statements(self):
        return filter(lambda y: isinstance(y, Statement), self.objs)

    @property
    def variables(self):
        vars = filter(lambda x: isinstance(x, Variable), self.objs)
        loops = filter(lambda x: isinstance(x, LoopNode) and x.kind == "for", self.objs)
        for loop in loops:
            if not loop.idx.declared:
                vars.append(loop.idx)
        return vars


class Expression(CodeObj):

    name = "expression"


class Statement(Expression):

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

    def __init__(self, var_name, var_type, var_init=NIL, **kws):
        super(Variable, self).__init__()
        self.generated = False
        self.declared = False
        self.var_name = var_name
        self.var_type = var_type
        self.var_init = var_init

    def __str__(self):
        return self.var_name

    def __add__(self, other):
        return Statement('+', self, other)


class IndexedVariable(Variable):
    """Represents a variable that can be indexed"""

    name = "indexed_variable"

    def __init__(self, var_name, var_type=None, shape=None, **kws):
        super(IndexedVariable, self).__init__(var_name, var_type, **kws)
        self.shape = shape

    def index_stmt(self, idx):
        """Returns a statement for indexing"""
        return Statement("index", self, idx)


class BlockNode(Expression):
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


class FunctionNode(BlockNode):
    """Represents a function block"""

    name = "functionnode"

    def __init__(self, func_name, ret_type=None, inputs=None, output=None,
                 member_function=False):
        super(FunctionNode, self).__init__()
        self.func_name = func_name
        self.ret_type = ret_type
        if ret_type is None and \
           output is not None and \
           output.var_type is not None:
            self.ret_type = output.var_type
        self.inputs = [] if inputs is None else inputs
        self.output = output
        self.member_function = member_function

    def add_return(self, variable):
        self.outputs.append(variable)


class ClassNode(BlockNode):
    """Represents a class block"""

    name = "classnode"

    def __init__(self, class_name, parents=None):
        super(ClassNode, self).__init__()
        self.members = OrderedDict([])
        self.classdict_members = OrderedDict()
        self.constructors = []
        self.class_name = class_name
        self.parents = parents if parents is not None else []

    def _add_member(self, odict, node):
        existing = odict.get(str(node))
        if existing == node:
            warnings.warn("Over writing known node: %s" % str(node),
                          RuntimeWarning, stacklevel=3)
        elif existing == node:
            pass
        else:
            node.class_member = True
            self.add_object(node)
            odict[str(node)] = node
        return self

    def add_classdict_member_function(self, func_node):
        return self._add_member(self.classdict_members, func_node)

    def add_classdict_member_variable(self, var_node):
        return self._add_member(self.classdict_members, var_node)

    def add_member_function(self, func_node):
        return self._add_member(self.members, func_node)

    def add_member_variable(self, var_node):
        return self._add_member(self.members, var_node)

    def create_constructor(self, *args, **kws):
        """Creates a constructor and adds to class node.

        See FunctionNode for keyword arguments.
        """
        node = FunctionNode("<constructor>", *args, **kws)
        node.class_member = True
        self.add_object(node)
        self.constructors.append(node)
        return node

    def get_member_variable(self, var_name, *args, **kws):
        ret_var = self.member.get(var_name)
        if ret_var is None:
            ret_var = Variable(var_name, *args, **kws)
            self.add_member_variable(ret_var)
        return ret_var

