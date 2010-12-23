from ignition import flatten

def test_flatten():
    assert(flatten([[1, [2, 3], [4, [5, [6, 7]]]], 8]) == range(9))
