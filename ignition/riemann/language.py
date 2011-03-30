"""Defines the Riemann language"""

from sympy import Matrix, Symbol

class Conserved (Symbol):
    def __new__(cls, name, dim=None):
        obj = Symbol.__new__(cls, name)
        obj.dim = dim
        obj._fields = None
        obj._field_names = None
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
            list_of_names = ["%s_%d" % (str(self._conserved), n) \
                             for n in xrange(self.dim)]
        if self.dim is not None and len(list(list_of_names)) != self.dim:
            raise ValueError("Given too many names for dim.")
        self._fields = map(Field, list_of_names)
        self._field_names = list_of_names
        return self._fields

    def jacobian(self, flux):
        if not self._fields:
            raise ValueError("No fields.")
        return Matrix(flux).jacobian(self._fields)

class Field (Symbol):
    pass

class ConstantField (Symbol):
    pass

class Constant (Symbol):
    pass

