"""General generators for SFL language"""

class SFLGenerator(object):
    """Base class for strong form language generator.

    """
    def __init__(self, expr):
        self.expr

    def generate(self):
        pass

class ProteusGenerator(SFLGenerator):
    """SFL generator for proteus framework

    """
    def to_file(self, filename):
        with f as open(filename, 'w'):
            f.write(self.generate)

class UFLGenerator(SFLGenerator):
    """SFL generator for UFL language

    """
    def to_file(self, filename):
        with f as open(filename, 'w'):
            f.write(self.generate)


def generator(framework, expr):
    """Generates the equation in a lower level framework"""
    if framework == "proteus":
        return ProteusGenerator(expr)
    
