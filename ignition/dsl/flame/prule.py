"""Module for base domian language and partition rules."""

class Rule (object):
    """Abstract object for providing mappings from different atoms to objects
    in a domain language."""
    def __new__ (cls):
        obj = object.__new__(cls)
        return obj

    def __call__ (self, *args, **kws):
        raise NotImplementedError

    def __iter__ (self, *args, **kws):
        raise NotImplementedError

    def __str__ (self):
        return "Rule()"

    def _latex (self):
        raise NotImplementedError

    def _ccode (self):
        raise NotImplementedError

    def _pycode (self):
        raise NotImplementedError

class PartRule (Rule):
    """Provides call backs to partition an atom in the domain language."""
    def __str__ (self):
        return "PartRule()"

    def _latex (self):
        return "Partition"

class RepartFuseRule (Rule):
    """Provides call backs to repartition a partition in the domain language."""
    def __str__ (self):
        return "RepartRule()"

    def _latex (self):
        return "Repartition"
