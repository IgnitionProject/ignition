"""Rules for symbolic tensor algebra"""

from sympy import Symbol, symbols

from tensor_expr import TensorExpr


m, n, k = symbols('mnk')

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

    def _set_default_shape(self, shape):
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

    def new (self, ind=None, transpose=None, hatted=None, rank=None,
             has_inverse=None):
        """Forms a new Tensor with only the listed attributes changed"""
        pass
