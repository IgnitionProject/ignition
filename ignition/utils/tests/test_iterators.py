from sympy import raises

from ignition.utils.iterators import UpdatingPermutationIterator


def test_UpdatingPermutationIterator ():
    iter = UpdatingPermutationIterator(range(2))
    assert(list(iter) == [[0, 1], [1, 0]])

    iter = UpdatingPermutationIterator(range(3))
    assert(iter.next() == [0, 1, 2])
    iter.bad_pos(0)
    assert(iter.next() == [1, 0, 2])
    iter.bad_pos(0)
    assert(iter.next() == [2, 0, 1])
