import numpy as np
from sympy import Add, Expr, Mul, Symbol


class StrongForm(object):

    def __init__(self, eqn):
        self.eqn = eqn

    def _find_obj(self, node, func, return_first=False):
        ret_set = set()
        if func(node):
            ret_set.add(node)
        if return_first and len(ret_set):
            return ret_set
        for arg in node.args:
            ret_set.update(self._find_obj(arg, func, return_first))
            if return_first and len(ret_set):
                return ret_set
        return ret_set

    def _find_obj_by_name(self, node, name):
        """Returns the first object with name"""
        func = lambda n: hasattr(n, "name") and n.name == name
        ret = self._find_obj(node, func, return_first=True)
        if len(ret):
            ret = ret.pop()
        else:
            ret = None
        return ret

    def _find_obj_by_type(self, node, type):
        """Returns all variables in node of given type"""
        func = lambda n: isinstance(n, type)
        return self._find_obj(node, func)

    def __getattr__(self, key):
        obj = self._find_obj_by_name(self.eqn, key)
        if obj is None:
            raise AttributeError("%s not found in 'StrongForm' or %s" % (key, self.eqn))
        return obj

    def __setattr__(self, key, val):
        if key != "eqn":
            try:
                obj = self._find_obj_by_name(self.eqn, key)
                if hasattr(obj, "_set"):
                    obj._set(val)
                    return
            except AttributeError:
                pass
        super(StrongForm, self).__setattr__(key, val)

    def variables(self):
        return self._find_obj_by_type(self.eqn, Variable)

    def separate_by_order(self):
        ret_dict = {}
        #TODO: Pretty gorpy, should probably use a dynamic programming solution
        def _order_visitor(node):
            if isinstance(node, Add):
                return max(map(_order_visitor, node.args))
            elif isinstance(node, Mul):
                return sum(map(_order_visitor, node.args))
            elif isinstance(node, Operator):
                return _order_visitor(node.args[0]) + node.differential_order
            else:
                return 0
        if isinstance(self.eqn, Add):
            for arg in self.eqn.args:
                order = _order_visitor(arg)
                ret_dict[order] = ret_dict.get(order, []) + [arg]
        else:
            order = _order_visitor(arg)
            ret_dict[order] = ret_dict.get(order, []) + [self.eqn]
        return ret_dict

    def extract_coefficients(self):
        ret_dict = {}
        order_dict = self.separate_by_order()
        return ret_dict


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
    differential_order = 0


class div(Operator):

    differential_order = 1

    def _latex(self, *args, **kws):
        from sympy import latex
        return "\div " + latex(self.args[0])


class grad(Operator):

    differential_order = 1


class Dt(Operator):
    """Derivative with respect to time."""

    differential_order = 1


class Dx(Operator):
    """Deriviative with repect to space."""

    differential_order = 1


class Dn(Operator):
    """Deriviative along normal of boundary."""

    differential_order = 1


class curl(Operator):

    differential_order = 1


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
        map(lambda name: obj(name, *args, **kws), name_str.split(kws.get('sep',' ')))
    f.__doc__ = "Calls %(obj_class)r on names in name_str.\n\n"\
                "See %(obj_class)r docstring for more details of args and kws" \
                % {"obj_class": obj}
    return f

Variables = _pluralize_obj_creation(Variable)
Constants = _pluralize_obj_creation(Constant)
Coefficients = _pluralize_obj_creation(Coefficient)
