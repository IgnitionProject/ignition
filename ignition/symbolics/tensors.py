"""Rules for symbolic tensor algebra"""

import operator

from sympy import Add, Basic, Expr, expand, Function, Mul, Number, Pow, \
    S, Symbol, symbols

DEBUG = False
m, n, k = symbols('mnk')

class NotInvertibleError (Exception):
    pass

class ConformityError (Exception):
    pass

class NonLinearEqnError (Exception):
    pass

class UnsolvableEqnsError (Exception):
    pass

class TensorExpr (Expr):
    """Base object for things with Tensor properties such as:
    * rank
    * shape
    * has_inverse
    * algebraic ops ( + - * / )
    """
    _op_priority = 20
    rank = -1
    name = None
    has_inverse = False
    shape = None
    is_symmetric = True

    def __mul__ (self, other):
#        print "calling TensorExpr.__mul__(", self, ",", other, ")"
        if isinstance(other, TensorExpr):
            if self.name == '0' or other.name == '0':
                r = self.rank + other.rank - 2
                if self.rank == 0:
                    r = other.rank
                elif other.rank == 0:
                    r = self.rank
                return Tensor('0', rank=r)
        if self.rank == 1 and expr_rank(other) == 1 \
            and self.shape == (1, n) and expr_shape(other) == (n, 1):
                return Inner(self, other)
        return super(TensorExpr, self).__mul__(other)

    def __rmul__ (self, other):
#        print "calling TensorExpr.__rmul__(", self, ",", other, ")"
        if isinstance(other, TensorExpr):
            if self.name == '0' or other.name == '0':
                r = self.rank + other.rank - 2
                if self.rank == 0:
                    r = other.rank
                elif other.rank == 0:
                    r = self.rank
                return Tensor('0', rank=r)
        if self.rank == 1 and expr_rank(other) == 1 \
            and self.shape == (n, 1) and expr_shape(other) == (1, n):
                return Inner(other, self)
        return super(TensorExpr, self).__rmul__(other)


    def __add__ (self, other):
        if self.name == '0':
            return other
        if isinstance(other, Tensor):
            if other.name == '0':
                return self
            if self.rank != other.rank:
                raise TypeError("Tensor addition only defined for same rank")

        return super(TensorExpr, self).__add__(other)

    def __radd__ (self, other):
        if self.name == '0':
            return other
        return super(TensorExpr, self).__radd__(other)

    def __div__ (self, other):
        if self.name == '0':
            raise ZeroDivisionError()
        if isinstance(other, TensorExpr):
            return Mul(self, Inverse(other))
        return super(TensorExpr, self).__div__(other)

    def __rdiv__ (self, other):
        if self.name == '0':
            raise ZeroDivisionError()
        return Mul(other, Inverse(self))

    def __pow__ (self, other):
        if self.name == '0':
            return self
        elif isinstance(other, int) and other < 0:
            return Inverse(self) ** (-other)
        else:
            return Pow(self, other)

    def __rpow__ (self, other):
        raise RuntimeError("Can't raise to the tensor power.")

class Tensor (TensorExpr, Symbol):
    """Basic Tensor symbol.
    >>> A = Tensor('A', rank=2)
    >>> B = Tensor('B', rank=2)
    >>> x = Tensor('x', rank=1)
    >>> y = Tensor('y', rank=1)
    >>> alpha = Tensor('alpha', rank=0)
    >>> beta = Tensor('beta', rank=0)
    >>> alpha*A*x + beta*B*x
    alpha*A*x + beta*B*x
    >>> expand((alpha*A+beta*B)*(x+y))
    alpha*A*x + alpha*A*y + beta*B*x + beta*B*y
    """

    def __new__ (cls, ten, rank=None, shape=None, has_inv=None, transposed=None,
                 **kws):
        if isinstance(ten, str):
            name = ten
            if rank is None:
                raise ValueError("Must give rank with string arg.")
            if rank == 0:
                has_inv = True
            elif has_inv is None:
                has_inv = False

        elif isinstance(ten, Tensor):
            name = ten.name
            if has_inv is None:
                has_inv = ten.has_inverse
            if not rank is None and rank != ten.rank:
                raise ValueError("Given rank and rank of ten don't match")
            if shape is None and transposed is None:
                shape = ten.shape
            if transposed is None:
                transposed = ten.transposed
            rank = ten.rank
        else:
            raise ValueError("Unable to create Tensor from a %s" \
                             % type(ten))
        has_inv = kws.get("has_inverse", has_inv)
        if rank > 0 and not kws.has_key("commutative"):
            kws['commutative'] = False

        if transposed is None:
            transposed = False
        if transposed:
            name += "'"

        obj = Symbol.__new__(cls, name, **kws)
        obj.rank = rank
        obj.has_inverse = has_inv
        obj.transposed = transposed

#        print "Transposed", transposed
        if rank == 0:
            obj.shape = (1, 1)
        elif rank == 1 and shape is None:
            if transposed:
                obj.shape = (1, n)
            else:
                obj.shape = (n, 1)
        elif rank == 2 and shape is None:
            obj.shape = (n, n)
        else:
            obj.shape = shape
        return obj

class Inverse (TensorExpr, Function):
    nargs = 1

    def __new__ (cls, arg, **options):
        if isinstance(arg, Inverse):
            return arg.args[0]
        arg_rank = expr_rank(arg)
        if arg_rank == 1:
            raise NotInvertibleError
        if isinstance(arg, Tensor) and arg.name == '0':
            raise NotInvertibleError
        if isinstance(arg, TensorExpr) and not arg.has_inverse:
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
        return "(" + str(self.args[0]) + "**-1)"

    def _eval_expand_basic(self, deep=True, **hints):
        if isinstance(self.args[0], Mul):
            if reduce(lambda acc, m: acc and m.has_inverse(), self.args[0].args,
                      True):
                return Mul(*map(Inverse, reversed(self.args[0].args)))
        return self

class Transpose (TensorExpr, Function):
    nargs = 1

    def __new__(cls, arg, **options):
        if isinstance(arg, Transpose) and isinstance(arg.args[0], Tensor):
            return arg.args[0]
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

    def _eval_expand_basic(self, deep=True, **hints):
        if isinstance(self.args[0], Mul):
            return Mul(*map(Transpose, reversed(self.args[0].args)))
        if isinstance(self.args[0], Add):
            return Add(*map(Transpose, self.args[0].args))
        return self

# Syntactic Sugar rename Transpose to T
T = Transpose

class Inner (TensorExpr, Function):
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
        return "(" + str(self.args[0]) + '*' + str(self.args[1]) + ")"

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


def numpy_print(expr):
    dot_str = "dot(%s, %s)"
#    print "numpy_print: ", expr, type(expr)
    if isinstance(expr, Mul):
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

def expr_shape(eqn):
    """Returns the shape of a given expression

    Will raise ConformityError if expression does not conform.
    
    >>> A = Tensor('A', rank=2)
    >>> B = Tensor('B', rank=2)
    >>> x = Tensor('x', rank=1)
    >>> expr_shape(A+B)
    (n, n)
    >>> expr_shape((A+B)*x)
    (n, 1)
    >>> expr_shape(A*T(x))
    ---------------------------------------------------------------------------
    ConformityError                           Traceback (most recent call last)
    """
    if isinstance(eqn, TensorExpr):
        return eqn.shape
    if isinstance(eqn, (Number, Symbol)):
        return (1, 1)
    if isinstance(eqn, Add):
        #TODO: Check consistency
        return expr_shape(eqn.args[0])
    if isinstance(eqn, Mul):
        arg_shapes = map(expr_shape, eqn.args)
        arg_shapes = filter(lambda x: x != (1, 1), arg_shapes)
        if len(arg_shapes) == 0:
            return (1, 1)
        for n in xrange(len(arg_shapes) - 1):
            if arg_shapes[n][1] != arg_shapes[n + 1][0]:
                raise ConformityError()
        return (arg_shapes[0][0], arg_shapes[-1][1])
    if isinstance(eqn, Pow):
        if expr_rank(eqn.args[0]) == 1:
            raise ConformityError()
        return expr_shape(eqn.args[0])
    raise NotImplementedError("expr_shape can't handle: %s of type: %s" % \
                              (str(eqn), type(eqn)))



def expr_rank(eqn):
    """Returns the rank of a given expression

    Will raise ConformityError if expression does not conform.
    
    >>> A = Tensor('A', rank=2)
    >>> B = Tensor('B', rank=2)
    >>> x = Tensor('x', rank=1)
    >>> expr_rank(A+B)
    2
    >>> expr_rank((A+B)*x)
    1
    >>> expr_rank(A*T(x))
    ---------------------------------------------------------------------------
    ConformityError                           Traceback (most recent call last)
    """

    if isinstance(eqn, TensorExpr):
        return eqn.rank
    if isinstance(eqn, (Number, int, float)):
        return 0
    if isinstance(eqn, Add):
        #TODO: Check consistency
        return expr_rank(eqn.args[0])
    if isinstance(eqn, Mul):
        arg_shape = expr_shape(eqn)
        return sum(map(lambda x: x != 1, arg_shape))
    if isinstance(eqn, Pow) and eqn.args[1] == -1:
        return expr_rank(eqn.args[0])
#        arg_ranks = map(expr_rank, eqn.args)
#        arg_ranks = filter(lambda x: x != 0, arg_ranks)
#        if len(arg_ranks) == 0:
#            return 0
#        return reduce(lambda acc, r: acc + r - 2, arg_ranks, 2)
    raise NotImplementedError("expr_rank can't handle: %s of type: %s" % \
                              (str(eqn), type(eqn)))


def solve_vec_eqn(eqn, var):
    """Returns the solution to a linear equation containing Tensors
    
    Raises:
      NonLinearEqnError if the variable is detected to be nonlinear
      NotInvertibleError if an inverse is required that is not available
      NotImplementedError if operation isn't supported by routine     
    """
    if DEBUG:
        print "solve_vec_eqn: ", eqn, "for", var
    if var.rank != expr_rank(eqn):
        raise ValueError("Unmatched ranks of clauses")
    if eqn.as_poly(var).degree() > 1:
        raise NonLinearEqnError()

    def _solve_recur(expr, rhs=S(0)):
        expr = expand(expr)
        if expr == var:
            return rhs
        elif isinstance(expr, Mul):
            lhs = S(1)
            # Try by rank
            coeff = expr.coeff(var)
            coeff_rank = expr_rank(coeff)
            if coeff_rank == 0:
                rhs /= coeff
                for arg in expr.args:
                    if var in arg:
                        lhs *= arg
            elif coeff_rank == 1:
                raise NotInvertibleError(str(coeff) + " of " + str(expr))
            elif coeff_rank == 2:
                for arg in expr.args:
                    if var in arg:
                        lhs *= arg
                    else:
                        rhs /= arg
            return _solve_recur(lhs, rhs)
        elif isinstance(expr, Add):
            lhs = 0
            for arg in expr.args:
                if var in arg:
                    lhs += arg
                else:
                    rhs -= arg
            if isinstance(lhs, Add):
                coeff = lhs.coeff(var)
                if expand(coeff * var) == lhs:
                    rhs /= coeff
                    lhs = var
            return _solve_recur(lhs, rhs)
        else:
            raise NotImplementedError("Can't handle expr of type %s" % type(expr))
    return _solve_recur(expand(eqn))
