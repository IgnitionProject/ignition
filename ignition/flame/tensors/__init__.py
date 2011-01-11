"""Symbolic tensor library

Provides a small symbolic tensor library for use with flame algorithms.
"""

# Cyclic dependencies require this order.
from tensor_expr import (
    ConformityError, TensorExpr, is_zero, is_outer,
    is_inner, mul_rank, expr_shape, expr_rank)
from tensor import (Tensor)
from basic_operators import (NotInvertibleError, Inner, Inverse, Transpose, T)
from solvers import (all_back_sub, solve_vec_eqn)
from printers import (numpy_print)
from tensor_names import (convert_name, set_lower_ind, set_upper_ind, to_latex)
from constants import (I, One, one, ZERO, Zero, zero)
from iterative_prules import (Fuse_1x1, Part_1x1, Repart_1x1,
                              Fuse_1x3, Part_1x3, Repart_1x3,
                              Fuse_J_3x3, Part_J_3x3, Repart_J_3x3)
