"""Defines the Riemann language"""

from sympy import Matrix, Symbol

class Conserved (Symbol):
    """Represents a conserved variable

    For multi-dimension variables, the dimension can be set with fields
    or with dim.

    The given a list of expressions, jacobian will compute the jacobian of the
    expressions with respect to the fields of the conserved variable.

    Examples:

    >>> q = Conserved('q', dim=2)
    >>> q_0, q_1 = q.fields()
    >>> q.jacobian([.5*q_0+q_1, q_1**2])
    [0.5,     1]
    [  0, 2*q_1]
    >>> nq = Conserved('nq')
    >>> u, uh = nq.fields(['u', 'uh'])
    >>> nq.jacobian([.5*u+uh, uh**2])
    [0.5,    1]
    [  0, 2*uh]

    """
    def __new__(cls, name, dim=None):
        obj = Symbol.__new__(cls, name)
        obj.dim = dim
        obj._fields = None
        obj._field_names = None
        obj._constant_fields = None
        return obj

    def fields(self, list_of_names=None):
        """Generates and returns the fields inside the conserve fields.

        If list of names is given, the fields are named accordingly once
        initialized with different names the names field is ignored.

        If a dimension wasn't set when the Conserved object was constructed,
        the dimension is determined from the number of names.  If the number
        of names and the dimension are different, an error is thrown.
        """
        if self._fields and self._field_names:
            return self._fields
        if not list_of_names:
            list_of_names = ["%s_%d" % (str(self), n) \
                             for n in xrange(self.dim)]
        if self.dim is not None and len(list(list_of_names)) != self.dim:
            raise ValueError("Given too many names for dim.")
        self._fields = map(Field, list_of_names)
        self._field_names = list_of_names
        return self._fields

    def jacobian(self, flux):
        """Returns the jacobian of the flux expression with respect to the
        fields in the conserved variable."""
        if not self._fields:
            raise ValueError("No fields.")
        return Matrix(flux).jacobian(self._fields)

class Field (Symbol):
    """Represents a field of the conserved quantity."""
    pass

class ConstantField (Symbol):
    """Represents a field of constants defined on cells."""
    pass

class Constant (Symbol):
    """Represents a global constant."""
    pass

