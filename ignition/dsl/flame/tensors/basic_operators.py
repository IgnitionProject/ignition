"""Some basic tensor operators"""

import operator
from numpy import matrix
from sympy import Add, Basic, expand, Function, latex, Mul, Pow, S

from .tensor_expr import expr_rank, expr_shape, is_one, is_zero, TensorExpr
from .tensor import Tensor

INVERTIBLE = []

class NotInvertibleError (Exception):
    pass

class Inverse (TensorExpr, Function):
    """Represents the inverse of a tensor expr."""
    nargs = 1

    def __new__ (cls, arg, **options):
#        print "Inverse(", arg, ")"
#        print INVERTIBLE
        if isinstance(arg, Inverse):
            return arg.args[0]
        if arg.is_Number:
            return 1 / arg

        arg_rank = expr_rank(arg)
        if arg_rank == 1:
            raise NotInvertibleError

        if is_one(arg):
            return arg
        if is_zero(arg):
            raise NotInvertibleError

        # FIXME: Funky case trying to catch lower triangular or diagonal
        #        muls like T(P_0)*A*P_0
        if arg in INVERTIBLE:
            pass
        elif isinstance(arg, TensorExpr) and not arg.has_inverse:
            raise NotInvertibleError
        elif isinstance(arg, Mul):
            if arg.args[0] == S(-1):
                return - Inverse(reduce(operator.mul, arg.args[1:]))
        if not expr_invertible(arg):
            raise NotInvertibleError
        options['commutative'] = arg.is_commutative
        return Basic.__new__(cls, arg, **options)

    @property
    def is_commutative(self):
        return self.args[0].is_commutative

    @property
    def shape(self):
        return expr_shape(self.args[0])

    @property
    def rank(self):
        return expr_rank(self.args[0])

    has_inverse = True

    def _sympystr(self, printer):
        return "(%s)**-1" % str(self.args[0])

    #FIXME: Not sure why inverse is getting an extra arg here but just using a
    #       dummy until I figure out the issue.
    def _latex(self, printer, *args):
        if len(self.args[0].args) <= 1:
            return latex(self.args[0]) + "^{-1}"
        else:
            return "\\left(%s\\right)^{-1}" % latex(self.args[0])

    def _eval_expand_basic(self, deep=True, **hints):
        if isinstance(self.args[0], Mul):
            if reduce(lambda acc, m: acc and expr_invertible(m),
                      self.args[0].args, True):
                #print "Inverse(", self.args, ")._eval_expand_basic"
                return reduce(operator.mul, map(Inverse, reversed(self.args[0].args)))
        return self

class Transpose (TensorExpr, Function):
    """Represents the transpose of a tensor expr."""

    nargs = 1

    def __new__(cls, arg, **options):
        if isinstance(arg, Transpose) and isinstance(arg.args[0], Tensor):
            return arg.args[0]
        if isinstance(arg, matrix):
            new_arg = arg.copy().transpose()
            for i in xrange(new_arg.shape[0]):
                for j in xrange(new_arg.shape[1]):
                    new_arg[i, j] = Transpose(new_arg[i, j])
            return new_arg
        if isinstance(arg, Tensor):
            if arg.rank == 0:
                return arg
            if arg.name == '0' or arg.name == 'I':
                return arg
        if arg.is_Number:
            return arg
        if isinstance(arg, Mul):
            rank_0_objs = filter(lambda arg: expr_rank(arg) == 0, arg.args)
            if len(rank_0_objs) > 0:
                other_objs = filter(lambda arg: arg not in rank_0_objs, arg.args)
                return Mul(*rank_0_objs) * Transpose(Mul(*other_objs))
        if arg.is_Symbol and not isinstance(arg, TensorExpr):
            return arg
        return Basic.__new__(cls, arg, **options)

    def update(self, *args, **kws):
        return Transpose(self.args[0].update(*args, **kws))

    @property
    def is_commutative(self):
        return self.args[0].is_commutative

    @property
    def shape(self):
        return tuple(reversed(expr_shape(self.args[0])))

    @property
    def rank(self):
        return expr_rank(self.args[0])

    @property
    def has_inverse(self):
        if self.rank == 0:
            return True
        elif self.rank == 1:
            return False
        else:
            return reduce(lambda acc, x: acc and x.has_inverse, self.atoms(), True)

    def _sympystr(self, printer):
        return "T(" + str(self.args[0]) + ")"

    def _latex(self, printer):
        if len(self.args[0].args) <= 1:
            return latex(self.args[0]) + "^t"
        else:
            return "\\left(%s)\\right)^t" % latex(self.args[0])


    def _eval_expand_basic(self, deep=True, **hints):
        if isinstance(self.args[0], Mul):
            return Mul(*map(Transpose, reversed(self.args[0].args)))
        if isinstance(self.args[0], Add):
            return Add(*map(Transpose, self.args[0].args))
        return self

# Syntactic Sugar rename Transpose to T
T = Transpose

class Inner (TensorExpr, Function):
    """Represents the inner product of two tensor exprs."""

    nargs = 2

    is_commutative = True

    def __new__(cls, arg0, arg1, **options):
        new_args = [arg0, arg1]



        #check for T(x)*y and T(x)*A*y
        arg_list = list(arg0.args) + list(arg1.args)
        if len(arg_list) < 3 and \
            all(map(lambda x: isinstance(x, TensorExpr), arg_list)):
            txy = None
            A = None
            if isinstance(arg0, Transpose):
                if isinstance(arg1, Mul) and len(arg1.args) <= 2:
                    txy = [arg0.args[0]] + [arg1.args[-1]]
                    if len(arg1.args) == 2:
                        A = arg1.args[0]
            elif isinstance(arg0, Mul) and len(arg1.args) <= 2:
                if isinstance(arg0.args[0], Transpose) and isinstance(arg1, Tensor):
                    txy = [arg0.args[0].args[0], arg1]
                    if len(arg0.args) == 2:
                        A = arg0.args[1]
            if txy:
                stxy = sorted(txy, Basic.compare)
                if txy != stxy:
                    if not A:
                        return Inner(Transpose(stxy[0]), stxy[1])
                    if A and A.is_symmetric:
                        return Inner(Transpose(stxy[0]) * A, stxy[1])

#        if expr_rank(arg0) != 1 and expr_rank(arg1) != 1:
#            return Mul(arg0, arg1)
#        for n in xrange(len(new_args)):
#            if isinstance(new_args[n], Transpose):
#                new_args[n] = new_args[n].args[0]
        return Basic.__new__(cls, *new_args, **options)

    @property
    def shape(self):
        return (1, 1)

    @property
    def rank (self):
        return 0

    @property
    def has_inverse(self):
        return True

    def _sympystr(self, printer):
        return "(%s*%s)" % tuple(map(latex, self.args))

    def _latex(self, printer):
        return "%s %s" % tuple(map(latex, self.args))

    def _eval_expand_basic(self, deep=True, **hints):
        arg0 = expand(self.args[0])
        arg1 = expand(self.args[1])

        arg0_adds = [arg0]
        arg1_adds = [arg1]
        if isinstance(arg0, Add):
            arg0_adds = arg0.args
        if isinstance(arg1, Add):
            arg1_adds = arg1.args

        add_exprs = []
        for arg0 in arg0_adds:
            for arg1 in arg1_adds:
                add_exprs.append(Inner(arg0, arg1))

        ret_add_exprs = []
        for expr in add_exprs:
            coeffs = []
            arg0 = expr.args[0]
            arg1 = expr.args[1]
            if isinstance(arg0, Mul):
                arg0_coeffs = filter(lambda arg: expr_rank(arg) == 0, arg0.args)
                if len(arg0_coeffs) != 0:
                    coeffs.extend(arg0_coeffs)
                    arg0 = Mul(*filter(lambda arg: expr_rank(arg) != 0, arg0.args))
            if isinstance(arg1, Mul):
                arg1_coeffs = filter(lambda arg: expr_rank(arg) == 0, arg1.args)
                if len(arg1_coeffs) != 0:
                    coeffs.extend(arg1_coeffs)
                    arg1 = Mul(*filter(lambda arg: expr_rank(arg) != 0, arg1.args))
            if len(coeffs) == 0:
                ret_add_exprs.append(expr)
            else:
                ret_add_exprs.append(Mul(*(coeffs + [Inner(arg0, arg1)])))

        return Add(*ret_add_exprs)

def expr_invertible(expr):
    if expr.is_Number:
        return True
    if isinstance(expr, TensorExpr) and expr.has_inverse:
        return True
    elif isinstance(expr, Pow):
        return expr_invertible(expr.args[0])
    if isinstance(expr, Inverse):
        return True
    if expr in INVERTIBLE:
        return True
    er = expr_rank(expr)
    if er == 1:
        return False
    if is_one(expr):
        return True
    if is_zero(expr):
        return False
    # FIXME: Funky case trying to catch lower triangular or diagonal
    #        muls like T(P_0)*A*P_0
    if isinstance(expr, Mul):
        return reduce(lambda acc, x: acc and expr_invertible(x), expr.args, True)
    if isinstance(expr, Pow):
        return expr_invertible(expr.args[0])

def add_invertible(expr):
    global INVERTIBLE
    INVERTIBLE.append(expr)
