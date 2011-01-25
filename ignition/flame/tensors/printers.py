"""Simple printers for tensor expressions"""

import operator
from copy import copy
from sympy import Add, Number, Mul, Pow, S

from tensor_expr import expr_rank
from tensor import Tensor
from basic_operators import Inner, Inverse, Transpose

defaults = {"add" : " + ",
            "div_under_one": "1.0 / (%s)",
            "dot" : "(%s, %s)",
            "inverse" : "(%s)**-1",
            "neg" : "-",
            "name_attr" : "name",
            "pow" : "(%s)**%s",
            "transpose" : "T(%s)",
            }

def print_visitor(expr_to_print, str_dict):
    """Prints a tensor expression in with predefined strings in string dict.
    
    See default_strs for str_dict keys.
    """
    def _visit (expr):
        if expr is None:
            return ""
        elif isinstance(expr, (Number, float, int)):
            return str(expr)
        elif isinstance(expr, Mul):
            if expr.args[0] is S(-1):
                return str_dict["neg"] + _visit(-1 * expr)
            if len(expr.args) == 2:
                return str_dict["dot"] % tuple(map(_visit, expr.args))
            else:
                return str_dict["dot"] % (_visit(expr.args[0]),
                                          _visit(reduce(operator.mul,
                                                               expr.args[1:])))
        elif isinstance(expr, Add):
            return str_dict["add"].join(map(_visit, expr.args))
        elif isinstance(expr, Pow):
            if expr.args[1] == S(-1):
                return str_dict["div_under_one"] % _visit(expr.args[0])
            if expr_rank(expr.args[1]) == 0 or expr_rank(expr) == 0:
                return str_dict["pow"] % tuple(map(_visit, expr.args))
            else:
                raise NotImplementedError("Unable to print: %s" % expr)
        elif isinstance(expr, Inner):
            return str_dict["dot"] % (_visit(expr.args[0]),
                                      _visit(expr.args[1]))
        elif isinstance(expr, Transpose):
            if expr_rank(expr) == 0:
                return _visit(expr.args[0])
            else:
                return str_dict["transpose"] % _visit(expr.args[0])
        elif isinstance(expr, Inverse):
            er = expr_rank(expr)
            if er == 0:
                return str_dict["div_under_one"] % _visit(expr.args[0])
            elif er == 2:
                return str_dict["inverse"] % _visit(expr.args[0])
            else:
                raise NotImplementedError
        elif isinstance(expr, Tensor):
            return expr.__getattribute__(str_dict["name_attr"])
        else:
            raise NotImplementedError
    return _visit(expr_to_print)


def numpy_print(expr):
    """Prints a tensor expression in Python using numpy."""
    my_strs = copy(defaults)
    my_strs["dot"] = "dot(%s, %s)"
    my_strs["transpose"] = "(%s).transpose()"
    my_strs["inverse"] = "inv(%s)"
    return print_visitor(expr, my_strs)


def latex_print(expr):
    """Prints a tensor expression in Latex."""
    my_strs = copy(defaults)
    my_strs["dot"] = "%s %s"
    my_strs["inverse"] = "{%s}^{-1}"
    my_strs["name_attr"] = "latex"
    my_strs["transpose"] = "{%s}^t"
    my_strs["pow"] = "{%s}^{%s}"
    return print_visitor(expr, my_strs)


