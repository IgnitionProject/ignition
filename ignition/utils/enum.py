
# -*- coding: utf-8 -*-

# enum.py
# Part of enum, a package providing enumerated types for Python.
#
# Copyright © 2007–2009 Ben Finney <ben+python@benfinney.id.au>
# This is free software; you may copy, modify and/or distribute this work
# under the terms of the GNU General Public License, version 2 or later
# or, at your option, the terms of the Python license.
#
# This file is included in the ignition library under the Python license.
#
# Modified by Andy R. Terrel <aterrel@tacc.utexas.edu>, 2010


""" Robust enumerated type support in Python.

This package provides a module for robust enumerations in Python.

An enumeration object is created with a sequence of string arguments
to the Enum() constructor::

    >>> from enum import Enum
    >>> Colours = Enum('red', 'blue', 'green')
    >>> Weekdays = Enum('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

The return value is an immutable sequence object with a value for each
of the string arguments. Each value is also available as an attribute
named from the corresponding string argument::

    >>> pizza_night = Weekdays[4]
    >>> game_night = Weekdays['mon']
    >>> shirt_colour = Colours.green

The values are constants that can be compared only with values from
the same enumeration; comparison with other values will invoke
Python's fallback comparisons::

    >>> pizza_night == Weekdays.fri
    True
    >>> shirt_colour > Colours.red
    True
    >>> shirt_colour == "green"
    False

Each value from an enumeration exports its sequence index
as an integer, and can be coerced to a simple string matching the
original arguments used to create the enumeration::

    >>> str(pizza_night)
    'fri'
    >>> shirt_colour.index
    2
    
The object can also take a list or tuple argument for keys that map to the
same value. The key method will only return the first value in the argument, 
so to test inclusion use the keys method, which always returns a list:

    >>> multi = Enum(('foo', 'bar'), 'baz')
    >>> multi.foo == multi.bar
    True
    >>> str(multi.foo)
    'foo'
    >>> 'foo' in multi.foo.keys
    True
    >>> 'baz' in multi.foo.keys
    False
"""


__author_name__ = "Ben Finney <ben+python@benfinney.id.au>"
__mod_author_name__ = "Andy R. Terrel <aterrel@tacc.utexas.edu>"
__copyright__ = "Copyright (C) 2007 -- 2009 %(__author_name__)s\n"\
                "  modified by %(__mod_author_name__)s, 2010\n" % vars()
__license__ = "Python license"

__url__ = "http://pypi.python.org/pypi/enum/"
__version__ = "0.4.4+"


from copy import copy

class EnumException(Exception):
    """ Base class for all exceptions in this module. """

    def __init__(self, *args, **kwargs):
        if self.__class__ is EnumException:
            class_name = self.__class__.__name__
            raise NotImplementedError(
                "%(class_name)s is an abstract base class" % vars())
        super(EnumException, self).__init__(*args, **kwargs)


class EnumEmptyError(AssertionError, EnumException):
    """ Raised when attempting to create an empty enumeration. """

    def __str__(self):
        return "Enumerations cannot be empty"


class EnumBadKeyError(TypeError, EnumException):
    """ Raised when creating an Enum with non-string keys. """

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return "Enumeration keys must be strings: %(key)r" % vars(self)


class EnumImmutableError(TypeError, EnumException):
    """ Raised when attempting to modify an Enum. """

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return "Enumeration does not allow modification"


def _comparator(func):
    """ Decorator for EnumValue rich comparison methods. """
    def comparator_wrapper(self, other):
        try:
            assert self.enumtype == other.enumtype
            result = func(self.index, other.index)
        except (AssertionError, AttributeError):
            result = NotImplemented

        return result
    comparator_wrapper.__name__ = func.__name__
    comparator_wrapper.__doc__ = getattr(float, func.__name__).__doc__
    return comparator_wrapper

class EnumValue(object):
    """ A specific value of an enumerated type. """

    def __init__(self, enumtype, index, key):
        """ Set up a new instance. """
        self._enumtype = enumtype
        self._index = index
        self._key = key

    @property
    def enumtype(self):
        return self._enumtype

    @property
    def key(self):
        if type(self._key) in [list, tuple]:
            return self._key[0]
        return self._key

    @property
    def keys(self):
        if type(self._key) in [list, tuple]:
            return list(self._key)
        return [self._key]

    def __str__(self):
        return str(self.key)

    @property
    def index(self):
        return self._index

    def __repr__(self):
        return "EnumValue(%(_enumtype)r, %(_index)r, %(_key)r)" % vars(self)

    def __hash__(self):
        return hash(self._index)

    @_comparator
    def __eq__(self, other):
        return (self == other)

    @_comparator
    def __ne__(self, other):
        return (self != other)

    @_comparator
    def __lt__(self, other):
        return (self < other)

    @_comparator
    def __le__(self, other):
        return (self <= other)

    @_comparator
    def __gt__(self, other):
        return (self > other)

    @_comparator
    def __ge__(self, other):
        return (self >= other)


class Enum(object):
    """ Enumerated type. """

    def __init__(self, *keys, **kwargs):
        """ Create an enumeration instance. """

        value_type = kwargs.get('value_type', EnumValue)

        if not keys:
            raise EnumEmptyError()

        keys = tuple(keys)
        values = [None] * len(keys)

        flat_keys = []
        flat_idx = []
        for i, key in enumerate(keys):
            values[i] = value_type(self, i, key)
            if type(key) in [list, tuple]:
                flat_keys += list(key)
                flat_idx += [i] * len(key)
            else:
                flat_keys.append(key)
                flat_idx.append(i)

        for i, key in zip(flat_idx, flat_keys):
            try:
                super(Enum, self).__setattr__(key, values[i])
            except TypeError:
                raise EnumBadKeyError(key)

        self.__dict__['_keys'] = flat_keys
        self.__dict__['_values'] = values

    @property
    def keys(self):
        return copy(self._keys)

    def __setattr__(self, name, value):
        raise EnumImmutableError(name)

    def __delattr__(self, name):
        raise EnumImmutableError(name)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        if type(index) is str:
            return self.__getattribute__(index)
        return self._values[index]

    def __setitem__(self, index, value):
        raise EnumImmutableError(index)

    def __delitem__(self, index):
        raise EnumImmutableError(index)

    def __iter__(self):
        return iter(self._values)

    def __contains__(self, value):
        is_member = False
        if isinstance(value, basestring):
            is_member = (value in self._keys)
        else:
            is_member = (value in self._values)
        return is_member


# Local variables:
# mode: python
# time-stamp-format: "%:y-%02m-%02d"
# time-stamp-start: "__date__ = \""
# time-stamp-end: "\"$"
# time-stamp-line-limit: 200
# End:
# vim: filetype=python fileencoding=utf-8 :
