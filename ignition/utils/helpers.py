"""Random helper routines not in standard python"""

def flatten (alst):
    """A recursive flattening algorithm for handling arbitrarily nested lists
    
    >>> flatten([0, [1,[2, 3], [4, [5, [6, 7]]]], 8])
    [1, 2, 3, 4, 5, 6, 7, 8]
    """
    def flatten_gen (lst):
        for elem in lst:
            if hasattr(elem, "__iter__"):
                for i in flatten(elem):
                    yield i
            else:
                yield elem
    return list(flatten_gen(alst))


