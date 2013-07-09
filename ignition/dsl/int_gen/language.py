"""Defines the IntGen (Integral Generator) language."""

import operator
from sympy import ccode

class IntGenExpr (object):
    """Base Expression Object"""
    def __new__ (cls, *args):
        obj = object.__new__(cls)
        obj._args = args
        return obj
    @property
    def args (self):
        return self._args

class Func (IntGenExpr):
    """Base Function object, also the symbolic function wrapper"""
    def __new__ (cls, sym_arg, var):
        return IntGenExpr.__new__(cls, sym_arg, var)
    def __mul__ (self, other):
        if isinstance(other, Func):
            return Mul(self, other)
        if isinstance(other, Dom):
            return Integral(self, other)
    def __add__ (self, other):
        if isinstance(other, Func):
            return Add(self, other)
    def __str__ (self):
        return str(self.args[0])
    def eval_str(self, dom, idx_str="i", qd_pt_str="QUAD_PTS"):
        qd_id_str = "(%(jac)f*%(qd_pt_str)s[%(idx_str)s]+%(shift)f)" % \
            {"qd_pt_str":qd_pt_str,
             "idx_str":idx_str,
             "jac":(dom.args[2] - dom.args[1]) / 2.0 ,
             "shift":(dom.args[2] + dom.args[1]) / 2.0 }
        return ccode(self.args[0]).replace(str(self.args[1]), qd_id_str)
    def eval_pt(self, qd_idx, pt):
        return self.args[0].subs(self.args[1], pt).evalf(), None

class Mul (Func):
    """Function multiplication"""
    def __new__  (cls, *args):
        if len(args) == 1:
            return args[0]
        elif len(args) < 1:
            return None
        if all(map(lambda a: type(a) == Func, args)):
            #TODO: Check for consistent variables
            return Func(reduce(operator.mul, [a.args[0] for a in args]), \
                        a.args[1])
        return IntGenExpr.__new__(cls, *args)
    def __str__(self):
        return " * ".join(map(str, self.args))
    def eval_str(self, dom, idx_str, qd_pt_str):
        return "*".join(map(lambda a:a.eval_str(dom, idx_str, qd_pt_str), self.args))
    def eval_pt(self, qd_idx, pt):
        nums, arrays = zip(*map(lambda arg: arg.eval_pt(qd_idx, pt), self.args))
        return reduce(operator.mul, nums), "*".join(filter(lambda a: a is not None, arrays))


class Add (Func):
    """Function addition"""
    def __new__ (cls, *args):
        if len(args) == 1:
            return args[0]
        elif len(args) < 1:
            return None
        if all(map(lambda a: type(a) is Func, args)):
            return Func(sum([a.args[0] for a in args]), args[0].args[1])
        return IntGenExpr.__new__(cls, *args)
    def __str__(self):
        return " + ".join(map(str, self.args))
    def eval_str(self, dom, idx_str, qd_pt_str):
        return "+".join(map(lambda a:a.eval_str(dom, idx_str, qd_pt_str), self.args))
    def eval_pt(self, qd_idx, pt):
        na_tuples = map(lambda arg: arg.eval_pt(qd_idx, pt), self.args)
        disc_eval = ""
        for i, (n, a) in enumerate(na_tuples):
            if i != 0:
                disc_eval += " + "
            if a is None:
                disc_eval += str(n)
            elif abs(n - 1.0) < 1e-10:
                disc_eval += a
            else:
                disc_eval += str(n) + '*' + a
        return 1.0, disc_eval

class DiscFunc (Func):
    """A discrete function"""
    def __new__ (cls, vec_name):
        return IntGenExpr.__new__(cls, vec_name)
    def __str__(self):
        return "DiscFunc(%s)" % self.args[0]
    def eval_str(self, dom, idx_str, qd_pt_str):
        return "%(vec_name)s[%(idx_str)s]" % \
                {"vec_name":self.args[0], "idx_str":idx_str}
    def eval_pt(self, qd_idx, pt):
        return 1.0, "%(name)s[%(idx)d]" % {"name":self.args[0], "idx":qd_idx}


class Dom (IntGenExpr):
    """The domain"""
    def __new__ (cls, var, start, stop):
        args = []
        if var: args.append(var)
        if start != None and stop != None: args.extend([start, stop])
        return IntGenExpr.__new__(cls, *args)

    def __rmul__ (self, integrand):
        return Integral(integrand, self)
    def __str__(self):
        return str(self.args)

class Integral (IntGenExpr):
    """An integral"""
    def __new__ (cls, func, domain):
        return IntGenExpr.__new__(cls, func, domain)
