"""Definition of code printers for PyClaw"""

import sympy as sp

from ...code_tools import indent_code
from .riemann_printer import RiemannPrinter

numerical_eigen_decomp = """
# Numerically solve eigenvalue decomposition
A = %s
eigen_vals, Rinv = np.linalg.eig(A)
R = np.linalg.inv(Rinv)
lam = np.diag(eigen_vals)
"""

symbolic_eigen_decomp = """
# Compute symbolic eigen decomposition
A = %s
R = %s
Rinv = %s
eigen_vals = %s
lam = np.diag(eigen_vals)
"""

pointwise_kernel = """
# Pointwise kernel
alpha = np.dot(Rinv,(q_r - q_l))
wave = R*np.diag(np.ravel(alpha))
lam_neg = np.diag(map(lambda x: 0.0 if x > -1e-10 else x, eigen_vals))
lam_pos = np.diag(map(lambda x: 0.0 if x < 1e-10 else x, eigen_vals))
amdq = wave*lam_neg
apdq = wave*lam_pos
"""

vectorized_symbolic_eigen_decomp = """
# Compute symbolic eigen decomposition
A = np.array([%s for rp in xrange(nrp)])
R = np.array([%s for rp in xrange(nrp)])
Rinv = np.array([%s for rp in xrange(nrp)])
eigen_vals = np.array([%s for rp in xrange(nrp)])
lam = np.array([np.diag(eigen_vals) for rp in xrange(nrp)])
"""

vectorized_numerical_eigen_decomp = """
# Numerically solve eigenvalue decomposition (vectorized version)
A = %s
eigen_vals = []; Rinv = []; R = []
for i in xrange(nrp):
    e, rinv = np.linalg.eig(A[i])
    r = np.linalg.inv(rinv)
    eigen_vals.append(e)
    Rinv.append(rinv)
    R.append(r)
"""

vectorized_shapes ="""
# Array shapes
meqn = %(meqn)d
mwaves = %(mwaves)d
nrp = np.size(q_l, 1)
"""

vectorized_kernel = """
# Vectorized kernel
dq = q_r - q_l
alpha = np.array([np.dot(Rinv[rp], dq[:,rp]) for rp in xrange(nrp)]).transpose()
#for rp in xrange(nrp):
#    for eqn in xrange(meqn):
#        wave[eqn, :, rp] = np.ravel(alpha[eqn,rp]*R[:,rp])
wave = np.array([R[rp]*np.diag(np.ravel(alpha[:,rp])) for rp in xrange(nrp)]).transpose()

amdq = np.zeros( (meqn, nrp) )
apdq = np.zeros( (meqn, nrp) )
for rp, ev in enumerate(eigen_vals):
    for n, e in enumerate(ev):
        if e < 0:
            amdq[:,rp] += e*wave[n,:,rp]
        elif e > 0:
            apdq[:, rp] += e*wave[n,:,rp]
"""

func_decl = """def kernel(q_l, q_r, aux_l, aux_r, aux_global):
"""

func_return = """return wave, eigen_vals, amdq, apdq
"""

vectorized_func_return = """return wave, eigen_vals.transpose(), amdq, apdq
"""

file_header = """from __future__ import division
import numpy as np
from numpy import sqrt

"""

class PyClawPrinter (RiemannPrinter):
    """Printer for pyclaw pointwise evaluation."""

    comment_str = "#"

    def _sympy_mat_to_numpy_str (self, mat):
        ret_code = "np.matrix(["
        ret_code += ", ".join(map(str, mat.tolist()))
        ret_code += "])"
        return ret_code

    def _print_constant_fields (self, indent=0):
        used_cf = self._generator.used_constant_fields()

        if len(used_cf) == 0:
            return ""

        ret_code = "\n# Evaluating Constant Fields\n"
        if self._generator.jacobian_averaging == "arithmetic":
            for n, cf in enumerate(self._generator.constant_fields):
                if cf in used_cf:
                    ret_code += "%(cf)s = (aux_l[%(n)d] + aux_r[%(n)d])" \
                                "/2.0\n" % {"cf":str(cf), "n":n}
        else:
            raise NotImplementedError("Unimplemented jacobian averaging: %s" \
                                      % self._generator.jacobian_averaging)
        return indent_code(ret_code, indent)

    def _print_constants (self, indent=0):
        ret_code = "\n# Evaluating Constants\n"
        for a in self._generator.used_constants():
            ret_code += "%(c)s = aux_global['%(c)s']\n" % {"c": str(a)}
        return indent_code(ret_code, indent)

    def _print_eigenvalues_symbolic (self, indent=0):
        ret_code = symbolic_eigen_decomp % \
                   (self._sympy_mat_to_numpy_str(self._generator.A),
                    self._sympy_mat_to_numpy_str(self._generator.R),
                    self._sympy_mat_to_numpy_str(self._generator.Rinv),
                    str(self._generator.eig_vals))
        return indent_code(ret_code, indent)

    def _print_eigenvalues_numerical (self, indent=0):
        A_str = self._sympy_mat_to_numpy_str(self._generator.A)
        ret_code = numerical_eigen_decomp % A_str
        return indent_code(ret_code, indent)

    def _print_evals (self, indent=0):
        ret_code = ""
        ret_code += self._print_constants(indent)
        ret_code += self._print_constant_fields(indent)
        ret_code += self._print_jac_evals(indent)
        return ret_code

    def _print_func_decl(self, indent=0):
        return indent_code(func_decl, indent)

    def _print_func_return(self, indent=0):
        return indent_code(func_return, indent)

    def _print_header(self, indent=0):
        return indent_code(file_header, indent)

    def _print_kernel (self, indent=0):
        return indent_code(pointwise_kernel, indent)

    def _print_kernel_file (self, indent=0):
        ret_code = ""
        ret_code += self._print_header(indent)
        ret_code += self._print_func_decl(indent)
        indent += 4
        ret_code += self._print_evals(indent)
        if self._generator.eig_method == "symbolic":
            ret_code += self._print_eigenvalues_symbolic(indent)
        elif self._generator.eig_method == "numerical":
            ret_code += self._print_eigenvalues_numerical(indent)
        ret_code += self._print_kernel(indent)
        ret_code += self._print_func_return(indent)
        return ret_code

    def _print_jac_evals (self, indent=0):
        if not self._generator._is_nonlinear():
            return ""

        ret_code = ""
        if self._generator.jacobian_averaging == "arithmetic":
            ret_code += "# Evaluate the averages of the conserved "\
                        "quantities\n"
            for n, f in enumerate(self._generator.conserved.fields()):
                ret_code += "%(f)s = (q_l[%(idx)d] + q_r[%(idx)d])/2.0\n" \
                            % {"f":str(f), "idx":n}
        else:
            raise NotImplementedError("Unimplemented jacobian averaging: %s" %\
                                      self._generator.jacobian_averaging)
        return indent_code(ret_code, indent)

class VectorizedPyClawPrinter (PyClawPrinter):
    """Printer for pyclaw vectorized evaluation."""

    def _sympy_mat_to_vectorized_numpy_str (self, mat):
        idx_field_subs = dict([(x, sp.Symbol(str(x) + "[i]")) \
                               for x in self._generator.conserved.fields()])
        return self._sympy_mat_to_numpy_str(mat.subs(idx_field_subs))

    def _print_constant_fields (self, indent=0):
        used_cf = self._generator.used_constant_fields()
        if len(used_cf) == 0:
            return ""

        ret_code = "\n# Evaluating Constant Fields\n"
        if self._generator.jacobian_averaging == "arithmetic":
            for n, cf in enumerate(self._generator.constant_fields):
                if cf in used_cf:
                    ret_code += "%(cf)s = (aux_l[%(n)d,:] + aux_r[%(n)d,:])" \
                                "/2.0\n" % {"cf":str(cf), "n":n}
        else:
            raise NotImplementedError("Unimplemented jacobian averaging: %s" \
                                      % self._generator.jacobian_averaging)
        return indent_code(ret_code, indent)

    def _print_eigenvalues_numerical (self, indent=0):
        sub_dict = {}
        for f in self._generator.conserved.fields() + \
                self._generator.used_constant_fields():
            sub_dict[f] = sp.Symbol(str(f)+"[rp]")
        A_str = "[%s for i in xrange(nrp)]" % \
                self._sympy_mat_to_vectorized_numpy_str( \
                    self._generator.A.subs(sub_dict))
        ret_code = vectorized_numerical_eigen_decomp % A_str
        return indent_code(ret_code, indent)

    def _print_eigenvalues_symbolic (self, indent=0):
        sub_dict = {}
        for f in self._generator.conserved.fields() +\
                self._generator.used_constant_fields():
            sub_dict[f] = sp.Symbol(str(f)+"[rp]")
        ret_code = vectorized_symbolic_eigen_decomp % \
                   (self._sympy_mat_to_numpy_str(self._generator.A.subs(sub_dict)),
                    self._sympy_mat_to_numpy_str(self._generator.R.subs(sub_dict)),
                    self._sympy_mat_to_numpy_str(self._generator.Rinv.subs(sub_dict)),
                    str([ev.subs(sub_dict) for ev in self._generator.eig_vals]))
        return indent_code(ret_code, indent)

    def _print_evals (self, indent=0):
        ret_code = ""
        ret_code += self._print_sizes(indent)
        ret_code += self._print_constants(indent)
        ret_code += self._print_constant_fields(indent)
        ret_code += self._print_jac_evals(indent)
        return ret_code

    def _print_func_return(self, indent=0):
        return indent_code(vectorized_func_return, indent)

    def _print_jac_evals (self, indent=0):
        ret_code = ""
        if self._generator._is_nonlinear():
            if self._generator.jacobian_averaging == "arithmetic":
                ret_code += "# Evaluate the averages of the conserved "\
                            "quantities\n"
                for n, f in enumerate(self._generator._conserved.fields()):
                    ret_code += "%(f)s = (q_l[%(idx)d,:] + q_r[%(idx)d,:])" \
                                "/2.0\n" % {"f":str(f), "idx":n}
            else:
                raise NotImplementedError("Unknown jacobian evaluation: %s" \
                                          % self._generator.jacobian_averaging)
        return indent_code(ret_code, indent)

    def _print_sizes (self, indent=0):
        meqn = len(self._generator.conserved.fields())
        mwaves = meqn
        return indent_code(vectorized_shapes % {"meqn":meqn, "mwaves":mwaves},
                           indent)

    def _print_kernel (self, indent=0):
        ret_code = vectorized_kernel
        return indent_code(ret_code, indent)
