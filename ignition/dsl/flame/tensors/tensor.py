"""Rules for symbolic tensor algebra"""

from sympy import Symbol, symbols
from sympy.core.decorators import call_highest_priority


from .tensor_expr import TensorExpr
from .tensor_names import add_idx, convert_name, set_lower_ind, set_upper_ind, \
                         to_latex


m, n, k = symbols('m n k')

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

        # Handle either str or change the behavior
        if isinstance(ten, str):
            name = ten
            if rank is None:
                raise ValueError("Must give rank with string arg.")
            if name in ['0', '1']:
                name = "%s_%d" % (name, rank)

            if name.startswith('0'):
                has_inv = False
            elif name.startswith('1') and rank in [0, 2]:
                has_inv = True
            elif rank == 0:
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
        obj._set_default_shape(shape)
        return obj

    def _set_default_shape (self, shape):
        if self.rank == 0:
            self.shape = (1, 1)
        elif self.rank == 1 and shape is None:
            if self.transposed:
                self.shape = (1, n)
            else:
                self.shape = (n, 1)
        elif self.rank == 2 and shape is None:
            self.shape = (n, n)
        else:
            self.shape = shape

    @property
    def latex (self):
        return to_latex(self.name)

    def _latex(self, printer):
        return self.latex

    def update (self, name=None, l_ind=None, u_ind=None, rank=None,
             has_inverse=None, shape=None, conform_name=True):
        """Forms a new Tensor with only the listed attributes changed"""
        name = self.name if name is None else name
        if l_ind is not None:
            name = set_lower_ind(name, l_ind)
        if u_ind is not None:
            name = set_upper_ind(name, u_ind)
        rank = self.rank if rank is None else rank
        if conform_name:
            name = convert_name(name, rank)
        return Tensor(name, rank=rank, shape=shape, has_inv=has_inverse)

class BasisVector (Tensor):
    """Unit basis vector with 1 at given position r.

    >>> e_0 = BasisVector(0)
    >>> A = Tensor('A')
    >>> A*e_0
    a[0]

    """

    _op_priority = 122

    def __new__ (cls, pos_or_ten, shape=None, **kws):
        if isinstance(pos_or_ten, Tensor) and pos_or_ten.rank == 1:
            return pos_or_ten
        elif not isinstance(pos_or_ten, int):
            raise ValueError("Must give either tensor or position, given %s" % \
                             str(pos_or_ten))
        obj = Tensor.__new__(cls, add_idx("e", pos_or_ten), rank=1)
        obj.idx = pos_or_ten
        return obj

    @call_highest_priority('__rmul__')
    def __mul__ (self, other):
        print "Inside BasisVector.__mul__"
        return super(BasisVector, self).__mul__(other)

    @call_highest_priority('__mul__')
    def __rmul__ (self, other):
        print "Inside BasisVector.__rmul__"
        if isinstance(other, Transpose) and isinstance(other.args[0], BasisVector):
            if other.args[0].idx == self.idx:
                return one
            else:
                return zero
        if isinstance(other, Tensor):
            ero = other.rank
            eso = other.shape
            if ero == 2:
                return other.update(add_idx(other.name, self.idx), rank=1)
            if ero == 1 and eso == (1, n):
                return other.update(add_idx(other.name, self.idx), rank=0)
        return super(BasisVector, self).__rmul__(other)


from .basic_operators import Transpose
from .constants import one, zero

