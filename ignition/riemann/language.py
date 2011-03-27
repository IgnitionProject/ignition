"""Defines the Riemann language"""

from sympy import Matrix, Symbol

class Conserved (Symbol):
    def __new__(cls, name, dim=None):
        obj = Symbol.__new__(cls, name)
        obj.dim = dim
        obj._fields = None
        return obj

    def fields(self, names):
        """Generates and returns names of fields inside the conserve field"""
        if self._fields:
            return self._fields
        if self.dim is not None and len(list(names)) != self.dim:
            raise ValueError("Given too many names for dim.")
        self._fields = map(Field, names)
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

