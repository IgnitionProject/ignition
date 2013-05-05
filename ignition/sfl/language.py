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

class FunctionSpace(Symbol):
    """Represents a function space"""
    pass

class Domain(Symbol):
    """Represents a domain"""
    pass

class Region(Domain):
    """Represents a region (or subset of a domain)"""
    pass

class Function(Symbol):
    pass

class Operator(Expr):
    pass


class div(Operator):
    pass

class grad(Operator):
    pass


class Dx(Operator):
    pass

class Dn(Operator):
    pass

class curl(Operator):
    pass

class rot(Operator):
    pass



class Coefficient(object):
    pass

class Constant(object):
    pass

class VectorConstant(object):
    pass

class TensorConstant(object):
    pass

class Measure(Symbol):
    pass

dX = Measure('dX')
