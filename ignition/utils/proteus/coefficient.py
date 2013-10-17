import sys

from ...dsl.sfl.generators import ProteusCoefficientGenerator


def sfl_coefficient(strong_form, *args, **kws):
    """Generates a proteus transport coefficient class from sfl and returns an
    instance of the class

    args and kws are passed to the constructor of that instance.
    """
    generator = ProteusCoefficientGenerator(strong_form)
    generator.to_file()
    sys.path.append(generator.module_path)
    mod = __import__(generator.module_name)
    coeff_instance = getattr(mod, generator.classname)(*args, **kws)
    coeff_instance.strong_form = strong_form
    return coeff_instance
