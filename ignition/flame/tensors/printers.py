import operator
from sympy import Add, Number, Mul, Pow, S

from tensor_expr import expr_rank
from tensor import Tensor
from basic_operators import Inner, Inverse, Transpose

def numpy_print(expr):
    dot_str = "dot(%s, %s)"
#    print "numpy_print: ", expr, type(expr)
    if isinstance(expr, (Number, float, int)):
        return str(expr)
    elif isinstance(expr, Mul):
        if expr.args[0] is S(-1):
            return "-" + numpy_print(-1 * expr)
        if len(expr.args) == 2:
            return dot_str % tuple(map(numpy_print, expr.args))
        else:
            return dot_str % (numpy_print(expr.args[0]),
                              numpy_print(reduce(operator.mul,
                                                 expr.args[1:])))
    elif isinstance(expr, Add):
        return " + ".join(map(numpy_print, expr.args))
    elif isinstance(expr, Pow):
        if expr.args[1] == S(-1):
            return "1.0 / %s" % numpy_print(expr.args[0])
        if expr_rank(expr) == 0:
            return "(%s)**%s" % tuple(map(numpy_print, expr.args))
        else:
            raise NotImplementedError
    elif isinstance(expr, Inner):
        if isinstance(expr.args[0], Transpose):
            return dot_str % (numpy_print(expr.args[0].args[0]),
                              numpy_print(expr.args[1]))
        else:
            return dot_str % (numpy_print(Transpose(expr.args[0])),
                              numpy_print(expr.args[1]))
    elif isinstance(expr, Transpose):
        if expr_rank(expr) == 0:
            return numpy_print(expr.args[0])
        else:
            return "(%s).transpose()" % numpy_print(expr.args[0])
    elif isinstance(expr, Inverse):
        er = expr_rank(expr)
        if er == 0:
            return "(1.0/%s)" % numpy_print(expr.args[0])
        elif er == 2:
            return "inv(%s)" % numpy_print(expr.args[0])
        else:
            raise NotImplementedError
    elif isinstance(expr, Tensor):
        return expr.name
    else:
        raise NotImplementedError
