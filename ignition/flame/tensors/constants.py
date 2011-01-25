""" Some useful constants """

from tensor import Tensor

ZERO = Tensor('0', 2)
Zero = Tensor('0', 1)
zero = Tensor('0', 0)

I = Tensor('1', 2)
One = Tensor('1', 1)
one = Tensor('1', 0)

CONSTANTS = set([ZERO, Zero, zero, I, One, one])
