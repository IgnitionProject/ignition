"""Symbolic tensor library

Provides a small symbolic tensor library for use with flame algorithms.
"""

# Cyclic dependencies require this order.
from tensor_expr import (
    ConformityError, TensorExpr, is_zero, is_outer,
    is_inner, mul_rank, expr_coeff, expr_shape, expr_rank)
from tensor import (Tensor)
from basic_operators import (NotInvertibleError, Inner, Inverse, Transpose, T)
from simplify import simplify
from solvers import (all_back_sub, tensor_solver, solve_vec_eqn)
from printers import (numpy_print, latex_print)
from tensor_names import (convert_name, set_lower_ind, set_upper_ind, to_latex)
from constants import (CONSTANTS, e, I, One, one, ZERO, Zero, zero)
from iterative_prules import * # FIXME: need real import here.
from args import iterative_arg
