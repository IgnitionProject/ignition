import numpy as np
from sympy import Expr, Symbol


class StrongForm(object):

    def __init__(self, eqn):
        self.eqn = eqn

    def _find_obj(self, name, node):
        if hasattr(node, "name") and node.name == name:
            return node
        for arg in node.args:
            obj = self._find_obj(name, arg)
            if obj is not None:
                return obj
        return None

    def __getattr__(self, key):
        obj = self._find_obj(key, self.eqn)
        if obj is None:
            raise AttributeError("%s not found in 'StrongForm' or %s" % (name, self.eqn))
        return obj

    def __setattr__(self, key, val):
        if key != "eqn":
            try:
                obj = self._find_obj(key, self.eqn)
                if hasattr(obj, "_set"):
                    obj._set(val)
                    return
            except AttributeError:
                pass
        super(StrongForm, self).__setattr__(key, val)


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
        obj = Variable.__new__(cls, 'time', space="L2")
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
    expr. Code linking to the generated code must define the named
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
    def __new__(cls, name, val=None, rank=None, dim=None):
        obj = Coefficient.__new__(cls, name, rank, dim)
        obj.val = np.array(val)
        return obj

    def _set(self, val):
        self.val = np.array(val)

class ChiConstant(Constant):
    """Represents a characteristic function"""
    pass


class RegionConstant(ChiConstant):
    """Represents a constant that is determined by the region of the domain"""
    pass


# Some utility functions
def _pluralize_obj_creation(obj):
    f = lambda name_str, *args, **kws: \
        map(lambda name: obj(name, *args, **kws), name_str.split())
    f.__doc__ = "Calls %(obj_class)r on names in name_str.\n\n"\
                "See %(obj_class)r docstring for more details of args and kws" \
                % {"obj_class": obj}
    return f

Variables = _pluralize_obj_creation(Variable)
Constants = _pluralize_obj_creation(Constant)
Coefficients = _pluralize_obj_creation(Coefficient)

# Visitors
def extract_independent_coefficients(expr):
    pass
