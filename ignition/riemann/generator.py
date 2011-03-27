"""Generator for simple Riemann solver"""
from ignition.riemann.language import Conserved

class Generator (object):
    def __init__ (self, flux, conserved):
        self._flux = flux
        self._conserved = conserved

    def _gen_A (self):
        return self.conserved.jacobian(self._flux)

    def _gen_eigenvalues (self):
        pass

    def _gen_numerical_eigen_code (self):
        pass

    def _gen_kernel_body (self):
        pass

    def generate(self):
        pass

    def write_to_file(self, filename=None):
        pass

def generate(flux, conserved, filename=None):
    """Generates the kernel to file (or stdout if no filename given)"""
    Generator(flux, conserved).write_to_file(filename)

flatte
