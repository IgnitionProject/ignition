import numpy as np

from ignition.flame.language import *
from ignition.symbolics.tensors import Tensor

def test_expressions():
    A = PObj("A", props=["Symmetric", "Invertible"])
    L = PObj("L", props=["LowerTriangular"])
    U = PObj("U", props=["UpperTriangular"])
    expr = A == L * U
    print expr


def test_part():
    A = PObj("A")
    B = PObj("B")
    A.part = np.matrix([Tensor("A", rank=2)])
    B.part = np.matrix([Tensor("B_L", rank=2), Tensor("B_R", rank=2)])
    print expr_part(A * B)

def test_repart():
    A = PObj("A")
    B = PObj("B")
    A_mat = Tensor("A", rank=2)
    B_L = Tensor("B_L", rank=2)
    B_R = Tensor("B_R", rank=2)

    A.part = np.matrix([A_mat])
    B.part = np.matrix([B_L, B_R])
    A.repart = {A_mat: A_mat}
    B.repart = {B_L: np.matrix([Tensor("B_0", rank=2)]),
                B_R: np.matrix([Tensor("b_1", rank=1), Tensor("B_2", rank=2)])}

    print expr_repart(A * B)

if __name__ == "__main__":
    #test_expressions()
    test_part()
