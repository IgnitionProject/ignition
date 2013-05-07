"""General generators for SFL language"""

class SFLGenerator(object):
    """Base class for strong form language generator.

    """
    def __init__(self, expr):
        self.expr = expr

    def generate(self):
        pass

class ProteusGenerator(SFLGenerator):
    """SFL generator for proteus framework

    """
    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate)

class UFLGenerator(SFLGenerator):
    """SFL generator for UFL language

    """
    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate)


def generate(framework, expr):
    """Generates the equation in a lower level framework"""
    if framework == "proteus":
        return ProteusGenerator(expr)
    
