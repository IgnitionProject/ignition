import importlib
import sys

from ignition.utils.code_obj import Statement
from ignition.utils.code_printer import CCodePrinter

from test_code_obj import create_sum_squares

def test_statement_C():
    dag = Statement('=', 'a', 'b')
    printer = CCodePrinter(dag)
    assert(printer.code_str() == "a = b;\n")

def test_sum_of_squares_C():
    """Test for compiling \sum_{i=1}^N i*i"""
    dag = create_sum_squares()
    cp = CCodePrinter(dag)
    module_name = "sum_of_squares"
    module_path = cp.to_ctypes_module(module_name)
    sys.path.append(module_path)
    sum_of_squares = importlib.import_module(module_name)
    assert(sum_of_squares.sum_squares(4) == 30)
