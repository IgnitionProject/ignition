import numpy as np
from sympy import Expr, Symbol

class Variable(Symbol):
    """Represents an unknown quantity"""
    def __new__(cls, name, dim=1, space="L2"):
        obj = Symbol.__new__(cls, name)
        obj.dim = dim
        obj.space = space
        return obj

class Time(Variable):
    """Special Variable representing time"""
    def __new__(cls):
        obj = Unknown.__new__(cls, 'time', space="L2")
        return obj

# Function space definition
class FunctionSpace(Symbol):
    """Represents a function space"""
    pass

# Domains
class Domain(Symbol):
    """Represents a domain"""
    pass

class Region(Domain):
    """Represents a region (or subset of a domain)"""
    pass

# Operators
class Operator(Expr):
    pass

class div(Operator):
    pass

class grad(Operator):
    pass

class Dt(Operator):
    """Derivative with respect to time."""
    pass

class Dx(Operator):
    """Deriviative with repect to space."""
    pass

class Dn(Operator):
    """Deriviative along normal of boundary."""
    pass

class curl(Operator):
    pass

class rot(Operator):
    pass


# Coefficients
class Coefficient(Symbol):
    """Represents a coefficient that is evaluated at quadrature points.

    Expression that is not defined by unknowns from another SFL
    expr. Code linking to the generated code must defind the named
    function for evaluation.
    """
    def __new__(cls, name, rank=None, dim=None):
        obj = Symbol.__new__(cls, name)
        obj.rank = rank
        return obj

class Constant(Coefficient):
    """Represents a constant coefficient that is evaluated at quadrature points.

    Expression that is not defined by unknowns from another SFL expr.
    """
    def __new__(cls, name, val, rank=None, dim=None):
        obj = Coefficient.__new__(cls, name, rank, dim)
        obj.val = np.array(val)
        return obj
