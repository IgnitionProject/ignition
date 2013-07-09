"""Simple printers for tensor expressions"""

import operator
from copy import copy
from sympy import Add, Number, Mul, latex, Pow, S

from tensor_expr import expr_rank
from tensor import Tensor
from basic_operators import Inner, Inverse, Transpose

defaults = {"add" : " + ",
            "div_under_one": "1.0 / (%s)",
            "dot" : "(%s, %s)",
            "inverse" : "(%s)**-1",
            "neg" : "-%s",
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
                return str_dict["neg"] % _wrap_parens(-1 * expr)
            if len(expr.args) == 2:
                return str_dict["dot"] % tuple(map(_wrap_parens, expr.args))
            else:
                return str_dict["dot"] % (_wrap_parens(expr.args[0]),
                                          _wrap_parens(reduce(operator.mul,
                                                               expr.args[1:])))
        elif isinstance(expr, Add):
            return str_dict["add"].join(map(_visit, expr.args))
        elif isinstance(expr, Pow):
            if expr.args[1] == S(-1):
                return str_dict["div_under_one"] % _wrap_parens(expr.args[0])
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
                return str_dict["transpose"] % _wrap_parens(expr.args[0])
        elif isinstance(expr, Inverse):
            er = expr_rank(expr)
            if er == 0:
                return str_dict["div_under_one"] % _wrap_parens(expr.args[0])
            elif er == 2:
                return str_dict["inverse"] % _wrap_parens(expr.args[0])
            else:
                raise NotImplementedError
        elif isinstance(expr, Tensor):
            return expr.__getattribute__(str_dict["name_attr"])
        else:
            raise NotImplementedError

    def _wrap_parens(expr):
        s = _visit(expr)
        if len(expr.args) <= 1 or (s[0] == '(' and s[-1] == ')'):
            return  s
        else:
            return "(%s)" % s

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
#    my_strs = copy(defaults)
#    my_strs["dot"] = "%s %s"
#    my_strs["inverse"] = "{%s}^{-1}"
#    my_strs["name_attr"] = "latex"
#    my_strs["transpose"] = "{%s}^t"
#    my_strs["pow"] = "{%s}^{%s}"
#    my_strs["div_under_one"] = "{%s}^{-1}"
#    return print_visitor(expr, my_strs)
    return latex(expr)

def wrap_long_latex_line(line, length=100):
    ret_val = ""
    while (len(line) > length):
        i = min(line.find(' + ', length), line.find(' - ', length))
        if i == -1:
            break
        nl = line[:i]
        line = line[i:]
        paren_mismatch = nl.count("\\left(") - nl.count("\\right)")
        if paren_mismatch > 0:
            nl += "\\right." * paren_mismatch
            line = "\\left." * paren_mismatch + line
        if paren_mismatch < 0:
            print "Unmatched parens somewhere."

        ret_val += nl
        ret_val += "\\\\\n  & &"
    return ret_val + line

def update_dict_to_latex(update_dict, order):
    """Returns update dictionary and order as latex string."""
    ret_val = "\\begin{eqnarray*}\n"
    get_line = lambda obj: wrap_long_latex_line(latex_print(obj) + "\\\\\n")
    for v in reversed(order):
        ret_val += latex_print(v) + " &=& "
        if isinstance(update_dict[v], set):
            if len(update_dict[v]) == 1:
                ret_val += get_line(list(update_dict[v])[0])
            else:
                for n, eq in enumerate(update_dict[v]):
                    ret_val += get_line(eq)
                    if n != len(update_dict[v]) - 1:
                        ret_val += " &||& "
        else:
            ret_val += get_line(update_dict[v])
    ret_val += "\\end{eqnarray*}\n"
#    ret_val = ret_val.replace('(', '\\left(')
#    ret_val = ret_val.replace(')', '\\right)')
#    ret_val = ret_val.replace('--', '')
    return ret_val
