from sympy.utilities.pytest import raises

from ignition.utils.iterators import (flatten, flatten_list, nested_list_idxs,
                                      UpdatingPermutationIterator)


def test_flatten():
    assert(flatten([0, [1, [2, 3], [4, [5, [6, 7]]]], 8]) == range(9))
    assert(flatten([0, (1, 2), [3, 4]]) == range(5))

def test_flatten_list():
    assert(flatten_list([0, [1, [2, 3], [4, [5, [6, 7]]]], 8]) == range(9))
    assert(flatten_list([0, (1, 2), [3, 4]]) == [0, (1, 2), 3, 4])

def test_nested_list_idxs():
    assert(nested_list_idxs([0, [1, [2]]]) == [(0,), (1, 0), (1, 1, 0)])

def test_UpdatingPermutationIterator ():
    iter = UpdatingPermutationIterator(range(2))
    assert(list(iter) == [[0, 1], [1, 0]])

    iter = UpdatingPermutationIterator(range(3))
    assert(iter.next() == [0, 1, 2])
    iter.bad_pos(0)
    assert(iter.next() == [1, 0, 2])
    iter.bad_pos(0)
    assert(iter.next() == [2, 0, 1])
