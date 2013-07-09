"""Module for simplifying Tensor exprs"""

import operator

from sympy import Add, Mul, Pow


from basic_operators import Inverse, Transpose, Inner

def simplify(expr, **kws):
    return simplify_mul_inverse(expr)

def simplify_mul_inverse(expr):
    if isinstance(expr, Add):
        return reduce(operator.add, map(simplify_mul_inverse,expr.args))
    if isinstance(expr, Pow):
        return simplify_mul_inverse(expr.args[0])**expr.args[1]
    if isinstance(expr, Mul):
        inv_idxs = filter(lambda n: isinstance(expr.args[n], Inverse),
                          xrange(len(expr.args)))
        for inv_idx in inv_idxs:
            arg = expr.args[inv_idx]
            arg_rank = arg.rank
            if arg_rank == 2:
                if inv_idx < len(expr.args) - 1 and expr.args[inv_idx+1] == arg.args[0]:
                    return simplify_mul_inverse(reduce(operator.mul,
                        expr.args[:inv_idx] + (One, ) + expr.args[inv_idx+2:]))
                if inv_idx > 0 and expr.args[inv_idx-1] == arg.args[0]:
                    return simplify_mul_inverse(reduce(operator.mul,
                        expr.args[:inv_idx-1] + (One, ) + expr.args[inv_idx+1:]))
            elif arg_rank == 0:
                for expr_idx in xrange(len(expr.args)):
                    if expr_idx != inv_idx and expr.args[expr_idx] == arg.args[0]:
                        f_idx = min(expr_idx, inv_idx)
                        s_idx = max(expr_idx, inv_idx)
                        return simplify_mul_inverse(reduce(operator.mul,
                            expr.args[:f_idx] + expr.args[f_idx+1: s_idx] + \
                            expr.args[s_idx+1:]))
    if isinstance(expr, (Inverse, Transpose, Inner)):
        return type(expr)(*map(simplify_mul_inverse, expr.args))

    else:
        return expr

