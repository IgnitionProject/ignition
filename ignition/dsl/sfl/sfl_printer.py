"""Base class for printers"""

from ...utils import comment_code, indent_code

class SFLPrinter(object):
    """Base class for all SFL printers"""
    
    def __init__(self, generator):
        self._generator = generator

    def print_file(self, indent=0):
        return comment_code(self._generator.info(), self.comment_str) + \
               self._print_file(indent)

    @staticmethod
    def get_printer(generator):
        """Returns a printer for generator object"""
        ret_obj = None
        language = generator.language
        if language == "ufl":
            ret_obj = UFLPrinter(generator)
        elif language == "proteus":
            ret_obj = ProteusScriptPrinter(generator)
        else:
            raise RuntimeError("No known printer for language %s" % language)

        return ret_obj

# Cyclic imports
#from ufl_printer import UFLPrinter
#from proteus_script_printer import ProteusScriptPrinter
