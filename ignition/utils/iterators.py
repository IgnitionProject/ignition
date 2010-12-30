"""Defines some custom iterators"""

from copy import copy

class UpdatingPermutationIterator (object):
    """A permutation iterator that can update to stop cycling on a particular
    position.
    
    >>> iter = UpdatingPermuataionIterator(range(2))
    >>> list(iter)
    [[0, 1], [1, 0]]
    >>> iter = UpdatingPermutationIterator(range(3))
    >>> iter.next()
    [0, 1, 2]
    >>> iter.bad_pos(0)
    >>> iter.next()
    [1, 0, 2]
    >>> iter.bad_pos(0)
    >>> list(iter)
    >>> [[2, 0, 1], [2, 1, 0]]
    
    
    """

    def __init__ (self, items, n= -1):
        self._items = copy(items)
        self._n = n if n > 0 and n <= len(items) else len(items)
        self._curr = range(self._n)
        self._done = False
        self._first = True

    def _increment(self):
        i = self._n - 1
        self._curr[i] += 1
        while i >= 0 and self._curr[i] > len(self._items) - 1:
            self._curr[i] = 0
            i -= 1
            if (i >= 0):
                self._curr[i] += 1
        if i < 0:
            self._done = True

    def _swap(self, i, j):
        tmp = self._curr[i]
        self._curr[i] = self._curr[j]
        self._curr[j] = tmp

    def _is_perm(self):
        return len(set(self._curr)) == len(self._curr)

    def __iter__ (self):
        return self

    def reset (self):
        self._curr = range(self._n)
        self._done = False
        self._first = True

    def next(self):
        if self._first:
            self._first = False
            return map(lambda idx: self._items[idx], self._curr)
        while not self._done:
            self._increment()
            if self._is_perm():
                ret_val = map(lambda idx: self._items[idx], self._curr)
                return ret_val
        raise StopIteration

    def bad_pos(self, pos):
        #find largest after bad pos
        if self._curr[pos] < len(self._items) - 1:
            self._curr[pos] += 1
            for idx in xrange(pos + 1, self._n):
                self._curr[idx] = 0
        elif pos == 0:
            self._done = True
        else:
            self._curr[pos - 1] += 1
            for idx in xrange(pos, self._n):
                self._curr[idx] = 0


def flatten (alst):
    """A recursive flattening algorithm for handling arbitrarily nested iterators
    
    >>> flatten([0, [1,(2, 3), [4, [5, [6, 7]]]], 8])
    [1, 2, 3, 4, 5, 6, 7, 8]
    """
    def _recur (blst):
        for elem in blst:
            if hasattr(elem, "__iter__"):
                for i in _recur(elem):
                    yield i
            else:
                yield elem
    return list(_recur(alst))

def flatten_list (alst):
    """Similar to flatten except only flattens lists
    
    >>> flatten_list([0, (2, 3), [4])
    [0, (2, 3), 4]
    """
    def _recur (blst):
        for elem in blst:
            if type(elem) is list:
                for i in _recur(elem):
                    yield i
            else:
                yield elem
    return list(_recur(alst))

def nested_list_idxs (alst):
    """Returns tuple generator corresponding to all indexes in the 
    nested list

    >>> list(nested_list_iter([[1,2],[3]])
    [(0,0), (0,1), (1,0)]
    """
    def _recur (blst, acc):
        if not type(blst) is list:
            return tuple(acc)
        else:
            ret_val = []
            for i in xrange(len(blst)):
                curr_acc = acc + [i]
                curr_val = _recur(blst[i], curr_acc)
                ret_val.append(curr_val)
            return ret_val
    return flatten_list(_recur(alst, []))
