"""Generator for simple Riemann solver"""

import numpy as np
import sympy as sp

from ...utils import flatten
from .language import Conserved, Constant, ConstantField
from .riemann_printer import RiemannPrinter

class SymbolicEigenDecompError (Exception):
    pass

class Generator (object):
    """Manager of the code generation of Riemann problem kernels of the form:

        q_t + f(q)*q_x = 0, or
        q_t + A * q_x = 0

    The conserved variable (q) and either the flux (f) or the jacobian (A) must
    be provided.  See either demos/Riemann or Riemann.language for defining
    these variables.

    Parameters (see `help(Generator.parameter)` for more details):

        conserved
            The conserved field passed to the generated kernel.
        flux
            The flux being solved.
        A
            The jacobian of the flux.
        constant_fields
            Constant fields used by generate passed via aux_{l,r}.
        eig_method
            Generation method for solving eigen decompostion of A.
        evaluation
            The evaluation type for single kernel.
        jacobian_averaging
            The method for averaging left and right values of a cell interface
            used in the kernel.
        language
            Language to generate.

    """

    def __init__ (self, **kws):
        self._kws = kws

    @property
    def conserved (self):
        """The conserved variable q of the hyperbolic system q_t + f(q)*q_x = 0."""
        return self._kws.get("conserved", None)

    @conserved.setter
    def conserved (self, value):
        self._kws["conserved"] = value

    @property
    def constant_fields (self):
        """The conserved variable q of the hyperbolic system q_t + f(q)*q_x = 0."""
        return self._kws.get("constant_fields", [])

    @constant_fields.setter
    def constant_fields (self, list_of_field_names):
        self._kws["constant_fields"] = map(ConstantFields, list_of_field_names)

    @property
    def flux (self):
        """The flux f(q) of the hyperbolic system q_t + f(q)*q_x = 0."""
        return self._kws.get("flux", None)

    @flux.setter
    def flux (self, value):
        self._kws["flux"] = value

    @property
    def A (self):
        """The jacobian of f(q) of the hyperbolic system q_t + f(q)*q_x = 0.

        If f is provided but not A, then A will be generated.
        """
        if self._kws.get("A", None) is None:
            self._kws["A"] = self.conserved.jacobian(self.flux)
        return self._kws["A"]

    @A.setter
    def A (self, value):
        self._kws["A"] = value

    @property
    def eig_method (self):
        """The method for the generating the eigen decomposition of A.

        Options:
            "analytic" - Using symbolic expression generate the analytic values
                of the eigenvalue decomposition.  Throws SymbolicEigenvalueError
                if unable to formulate the analytic eigen decomposition
            "numerical" - Generates a simple eigenvalue decomposition algorithm
                in the generated kernel.
            "auto" (default) - Tries symbolic generation but if it fails it a
                simple numerical eigen solver will be generated.
        """
        return self._kws.get("eig_method", "auto")

    @eig_method.setter
    def eig_method (self, value):
        self._kws["eig_method"] = value

    @property
    def evaluation (self):
        """The evaluation method of the generated kernel.

        Options:
            "pointwise" (default) - the kernel will expect a single point for
                left and right values of a cell.
            "vectorized" - the kernel will expect a vector of points for left
                and right values of cells.
        """
        return self._kws.get("evaluation", "pointwise")

    @evaluation.setter
    def evaluation (self, value):
        self._kws["evaluation"] = value

    @property
    def jacobian_averaging (self):
        """The jacobian_averaging method of the generated kernel.

        Options:
            "arithmetic" (default) - Any evaluation over a cell interface
                required by the jacobian will use an average of the left and
                right states.
            "LR_eigs" - A left and right jacobian will be formed and the
                eigen decomposition of each will operate on the appropriate
                plus or minus fluctuation (amdq or apdq).
        """
        return self._kws.get("jacobian_averaging", "arithmetic")

    @jacobian_averaging.setter
    def jacobian_averaging (self, value):
        self._kws["jacobian_averaging"] = value

    @property
    def language (self):
        """The language of the generated kernel.

        Options:
            "pyclaw" - Code generated to the Python interface of CLAWPACK.
        """
        return self._kws.get("language", "pyclaw")

    @language.setter
    def language (self, value):
        self._kws["language"] = value

    def _is_nonlinear (self):
        """Simple check for non-linear fluxes"""
        for field in self.conserved.fields():
            for term in flatten(self.A.tolist()):
                if field in term:
                    return True
        return False

    def _gen_eigenvalues (self):
        if self.eig_method in ["symbolic", "auto"]:
            try:
                eig_triples = self.A.eigenvects()
                mat_size = eig_triples[0][2][0].shape[0]
                R = np.empty((mat_size, mat_size), dtype=sp.Expr)
                self.eig_vals = []
                for col in xrange(len(eig_triples)):
                    evect = eig_triples[col][2][0]
                    for mult in xrange(eig_triples[col][1]):
                        self.eig_vals.append(eig_triples[col][0])
                        for row in xrange(mat_size):
                            R[row, col + mult] = evect[row]
                self.R = sp.Matrix(R)
                self.Rinv = self.R.inv()
                if self.eig_method == "auto":
                    self.eig_method = "symbolic"
            except IndexError:
                if self.eig_method == "symbolic":
                    raise SymbolicEigenDecompError()
                elif self.eig_method == "auto":
                    self.eig_method = "numerical"
        if self.eig_method == "numerical":
            pass
        if self.eig_method not in ["symbolic", "numerical", "auto"]:
            raise ValueError("Unknown eig_method: %s" % self.eig_method)

    def used_constants(self):
        """Constants used inside jacobian evaluation"""
        A = self.A
        atoms = set(flatten([x.atoms() for x in flatten(A.tolist())]))
        return filter(lambda a: isinstance(a, Constant), atoms)

    def used_constant_fields(self):
        """Constant Fields used inside jacobian evaluation"""
        A = self.A
        atoms = set(flatten([x.atoms() for x in flatten(A.tolist())]))
        return filter(lambda a: isinstance(a, ConstantField), atoms)

    def info (self):
        """Returns the parameters of the Riemann problem being generated."""
        ret_code = "Riemann Kernel generated from:\n"
        ret_code += " "*4 + "flux: %s\n" % str(self.flux)
        ret_code += " "*4 + "conserved: %s\n" % str(self.conserved)
        ret_code += " "*4 + "A: %s\n" % str(self.A)
        ret_code += " "*4 + "eig_method: %s\n" % str(self.eig_method)
        ret_code += " "*4 + "evaluation: %s\n" % str(self.evaluation)
        ret_code += " "*4 + "language: %s\n" % str(self.language)
        ret_code += " "*4 + "jacobian_averaging: %s\n" % \
                    str(self.jacobian_averaging)
        return ret_code

    def generate (self):
        """Returns the code for the kernel function."""
        self._gen_eigenvalues()
        printer = RiemannPrinter.get_printer(self)
        return printer.print_kernel_file()

    def write (self, filename=None):
        """Prints the generated kernel function to filename.

        If filename is None, the kernel is printed to stdout.
        """
        code = self.generate()
        if filename:
            print "Writing to file: %s" % filename
            with open(filename, 'w') as fp:
                fp.write(code)
        else:
            return code

def generate (filename=None, **kws):
    """Generates the kernel to file (or stdout if no filename given).

    For required keywords (kws) please see help(Generator).
    """
    Generator(**kws).write(filename)

