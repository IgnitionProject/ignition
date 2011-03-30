"""Generator for simple Riemann solver"""
from ignition.utils import flatten, indent_code

from language import Conserved, Constant, ConstantField
import pyclawpack_templates as pcp

class Generator (object):
    """Main object for managing the code generation."""

    def __init__ (self, flux, conserved):
        self._flux = flux
        self._conserved = conserved
        self._eig_method = "numerical"
        self._language = "python"
        self._conserved_jac = None

    def _get_A (self):
        if not self._conserved_jac:
            self._conserved_jac = self._conserved.jacobian(self._flux)
        return self._conserved_jac

    def _gen_eigenvalues (self, indent=0):
        ret_code = ""
        A = self._get_A()
        if self._eig_method == "numerical":
            if self._language == "python":
                A_str = "np.matrix(["
                A_str += ", ".join(map(str, A.tolist()))
                A_str += "])"
                ret_code = pcp.numerical_eigen_decomp % A_str
        return indent_code(ret_code, indent)

    def _gen_riemann_comp (self, indent=0):
        if self._language == "python":
            ret_code = pcp.pointwise_kernel
        return indent_code(ret_code, indent)

    def _gen_expand_constants (self, indent=0):
        ret_code = ""
        if self._language == "python":
            for n, f in enumerate(self._conserved.fields()):
                ret_code += "%(f)s = (q_l[%(idx)d] + q_r[%(idx)d])/2.0\n" % \
                    {"f":str(f), "idx":n}
        A = self._get_A()
        atoms = set(flatten([x.atoms() for x in flatten(A.tolist())]))
        for a in atoms:
            if isinstance(a, Constant):
                ret_code += "%(c)s = aux_global['%(c)s']\n" % \
                    {"c": str(a)}
#            if isinstance(a, ConstantField):
#                ret_code += "%(c)s = aux_r[%(idx)] - aux_l[%(idx)]\n"
        return indent_code(ret_code, indent)

    def _gen_kernel_func (self, indent=0):
        ret_code = ""
        if self._language == "python":
            ret_code = indent_code(pcp.func_decl, indent)
            ret_code += self._gen_expand_constants(indent + 4)
            ret_code += self._gen_eigenvalues(indent + 4)
            ret_code += self._gen_riemann_comp(indent + 4)
            ret_code += indent_code(pcp.func_return, indent + 4)
        return ret_code

    def generate(self):
        """Returns the generated kernel function."""
        return self._gen_kernel_func()

    def write_to_file(self, filename=None):
        """Prints the generated kernel function to filename
        (stdout if filname is None)"""
        print self.generate()

def generate(f, flux, conserved, filename=None):
    """Generates the kernel to file (or stdout if no filename given)"""
    Generator(flux, conserved).write_to_file(filename)

