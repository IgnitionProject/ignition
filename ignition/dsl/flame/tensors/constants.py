""" Some useful constants """

from .tensor import Tensor

ZERO = Tensor('0', 2)
Zero = Tensor('0', 1)
zero = Tensor('0', 0)

I = Tensor('1', 2)
One = Tensor('1', 1)
one = Tensor('1', 0)

e = Tensor('e', 1)

CONSTANTS = set([ZERO, Zero, zero, I, One, one, e])


# Not constants but putting here anyways
A = Tensor("A", rank=2)
P_0 = Tensor("P_0", rank=2)
