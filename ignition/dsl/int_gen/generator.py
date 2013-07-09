"""Defines the generators for the IntGen language."""

from math import sqrt
from sympy import ccode, sympify

from .language import Add, DiscFunc

QUAD_PTS = [-(1.0 / 3.0 * sqrt(5 + 2 * sqrt(10.0 / 7.0))),
            - (1.0 / 3.0 * sqrt(5 - 2 * sqrt(10.0 / 7.0))),
            0.0,
            1.0 / 3.0 * sqrt(5 - 2.0 * sqrt(10.0 / 7.0)),
            1.0 / 3.0 * sqrt(5 + 2.0 * sqrt(10.0 / 7.0))]
QUAD_WTS = [(322 - 13 * sqrt(70)) / 900,
            (322 + 13 * sqrt(70)) / 900,
            128.0 / 225.0,
            (322.0 + 13 * sqrt(70)) / 900,
            (322.0 - 13 * sqrt(70)) / 900]

def select_quad_rule (num_pts, name="Gauss"):
    """Simple selector for quadrature rules"""
    global QUAD_PTS, QUAD_WTS
    if name != "Gauss":
        raise NotImplementedError
    if num_pts == 1:
        QUAD_PTS = [0.0]
        QUAD_WTS = [2.0]
    elif num_pts == 2:
        QUAD_PTS = [-1.0 / sqrt(3), 1.0 / sqrt(3)]
        QUAD_WTS = [1.0, 1.0]
    elif num_pts == 3:
        QUAD_PTS = [-sqrt(15) / 5.0, 0.0, sqrt(15) / 5.0]
        QUAD_WTS = [5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0]
    elif num_pts == 4:
        QUAD_PTS = [-sqrt((3 + 2 * sqrt(6.0 / 5.0)) / 7.0),
                    - sqrt((3 - 2 * sqrt(6.0 / 5.0)) / 7.0),
                    sqrt((3 - 2 * sqrt(6.0 / 5.0)) / 7.0),
                    sqrt((3 + 2 * sqrt(6.0 / 5.0)) / 7.0)]
        QUAD_WTS = [(18.0 - sqrt(30) / 36.0),
                    (18.0 + sqrt(30) / 36.0),
                    (18.0 + sqrt(30) / 36.0),
                    (18.0 - sqrt(30) / 36.0)]
    elif num_pts == 5:
        QUAD_PTS = [-(1.0 / 3.0 * sqrt(5 + 2 * sqrt(10.0 / 7.0))),
            - (1.0 / 3.0 * sqrt(5 - 2 * sqrt(10.0 / 7.0))),
            0.0,
            1.0 / 3.0 * sqrt(5 - 2.0 * sqrt(10.0 / 7.0)),
            1.0 / 3.0 * sqrt(5 + 2.0 * sqrt(10.0 / 7.0))]
        QUAD_WTS = [(322 - 13 * sqrt(70)) / 900,
            (322 + 13 * sqrt(70)) / 900,
            128.0 / 225.0,
            (322.0 + 13 * sqrt(70)) / 900,
            (322.0 - 13 * sqrt(70)) / 900]
    else:
        raise NotImplementedError

def gen_file(name, integrals, func_names, input_vars):
    """Wrapper to generate numerous integrals in a single file."""
    indent = 0
    code = gen_header(name, indent)
    code += gen_QUAD_RULE(indent)
    for intgrl, fname, vars in zip(integrals, func_names, input_vars):
        code += int_gen(intgrl, fname, vars, indent)
    code += gen_footer(name)
    fp = open(name + ".h", 'w')
    fp.write(code)
    fp.close()

def gen_header(name, indent=0):
    return "#ifndef %(name)s\n#define %(name)s\n\n#include <math.h>\n\n" % \
            {"name":"__" + name.upper() + "__"}

def gen_footer(name, indent=0):
    return "#endif /* %(name)s */\n" % \
            {"name":"__" + name.upper() + "__"}

def gen_QUAD_RULE(indent):
    code = "const unsigned int NUM_QUAD_PTS = %(num_pts)s;\n" \
           "const double QUAD_PTS[%(num_pts)s] = {%(qd_pts)s};\n" \
           "const double QUAD_WTS[%(num_pts)s] = {%(qd_wts)s};\n\n"
    return code % {"num_pts":len(QUAD_PTS),
                   "qd_pts": ", ".join(map(str, QUAD_PTS)),
                   "qd_wts": ", ".join(map(str, QUAD_WTS))}

def int_gen(integral, func_name, input_vars, indent=0):
    """Main C code generator for a integral expression"""
    sym, disc = split_func(integral.args[0])
    ret_str = "ret_val"
    code = gen_fdec(func_name, input_vars, indent)
    indent += 1
    code += gen_init_var(ret_str, indent)
    code += gen_symbolic(sym, integral.args[1], ret_str, indent)
#    code += gen_discrete(disc, integral.args[1], ret_str, indent)
    code += gen_discrete_unrolled(disc, integral.args[1], ret_str, indent)
    code += gen_return_var(ret_str, indent)
    indent -= 1
    code += gen_fclose(indent)
    return code

def split_func (func):
    if is_symbolic(func):
        return func, None
    if isinstance(func, Add):
        syms = []
        evals = []
        for arg in func.args:
            sym, eval = split_func(arg)
            if sym: syms.append(sym)
            if eval: evals.append(eval)
        return Add(*syms), Add(*evals)
    return None, func

def is_symbolic(func):
    if isinstance(func, DiscFunc):
        return False
    return all(map(is_symbolic, func.args))

def gen_init_var(var, indent=0):
    return "%(indent)sdouble %(var)s = 0.0;\n" % \
            {"indent":" " * 2 * indent, "var":var}

def gen_return_var(var, indent=0):
    return "%(indent)sreturn %(var)s;\n" % \
            {"indent":" " * 2 * indent, "var":var}

def gen_fdec(func_name, input_vars, indent):
    return "%(ind)sdouble %(func_name)s(%(input_vars)s)\n%(ind)s{\n" % \
            {"ind":" " * 2 * indent,
             "func_name":func_name,
             "input_vars":", ".join(map(lambda x: "double* " + x, input_vars))}

def gen_fclose(indent=0):
    return "%(indent)s}\n\n" % {"indent":" " * 2 * indent}

def gen_symbolic(func, dom, ret_str="ret_val", indent=0):
    if func is None:
        return ""
    intgrl = sympify(func).integrate(dom.args)
    if intgrl is None:
        raise ValueError("Unable to integrate sym")
    else:
        return "%(indent)s%(ret_str)s += %(intgrl)s;\n" % \
            {"indent": " " * 2 * indent,
             "ret_str": ret_str,
             "intgrl": ccode(intgrl.evalf())}

def gen_discrete(func, dom, ret_str="ret_val", indent=0):
    if func is None:
        return ""
    return """
%(indent)sunsigned int i;
%(indent)sfor (i=0; i<NUM_QUAD_PTS; ++i)
%(indent)s  %(ret_str)s += QUAD_WTS[i]*(%(func_eval)s);
%(indent)sret_str *= %(jac)s
""" % \
    {"indent": " " * 2 * indent,
     "ret_str": ret_str,
     "func_eval": func.eval_str(dom, "i", "QUAD_PTS"),
     "jac":(dom.args[2] - dom.args[1]) / 2.0 }

def gen_discrete_unrolled(func, dom, ret_str="ret_val", indent=0):
    if func is None:
        return ""
    disc_eval = ""
    jac = (dom.args[2] - dom.args[1]) / 2.0
    shift = (dom.args[2] + dom.args[1]) / 2.0
    for i in xrange(len(QUAD_PTS)):
        num, array = func.eval_pt(i, jac * QUAD_PTS[i] + shift)
        if i != 0:
            disc_eval += "\n%s  + " % (" "*(indent * 2 + len(ret_str)))
        disc_eval += str(jac * num * QUAD_WTS[i]) + "*(" + array + ")"
    return """
%(indent)s%(ret_str)s += %(disc_eval)s;
""" % \
    {"indent": " " * 2 * indent,
     "ret_str": ret_str,
     "disc_eval": disc_eval}
