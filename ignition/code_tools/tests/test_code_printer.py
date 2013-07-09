from importlib import import_module
import sys

from ignition.code_tools.code_obj import Statement
from ignition.code_tools.code_printer import CCodePrinter

from test_code_obj import create_sum_squares, create_double_sum, create_index_variable_loop


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
    sum_of_squares = import_module(module_name)
    assert(sum_of_squares.sum_squares(4) == 30)

def test_double_sum_C():
    dag = create_double_sum()
    modname = "double_sum"
    modpath = CCodePrinter(dag).to_ctypes_module(modname)
    sys.path.append(modpath)
    double_sum = import_module(modname)
    assert(double_sum.double_sum(3) == 20)

def test_jndex_variable_loop_C():
    dag = create_index_variable_loop()
    modname = "index_variable_loop"
    modpath = CCodePrinter(dag).to_ctypes_module(modname)
    sys.path.append(modpath)
    index_variable_loop = import_module(modname)
    assert(index_variable_loop.idx_loop_fun() == 45)
