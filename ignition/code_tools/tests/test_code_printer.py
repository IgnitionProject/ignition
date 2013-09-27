from importlib import import_module
import os
import time
import tempfile
import sys

from ignition.code_tools.code_obj import Statement
from ignition.code_tools.code_printer import CCodePrinter, PythonCodePrinter

from test_code_obj import (create_class_obj, create_double_sum,
                           create_index_variable_loop, create_sum_squares)


TEST_DIR = ''
ROOT_DIR = ''


def setup_module():
    global ROOT_DIR
    ROOT_DIR = os.getcwd()
    global TEST_DIR
    time_str = time.strftime('%Y%m%d-%H:%M:%S')
    TEST_DIR = tempfile.mkdtemp(prefix="ignition-%s" % time_str)
    os.chdir(TEST_DIR)
    print("Generating files in: %s" % TEST_DIR)


def teardown_module():
    os.chdir(ROOT_DIR)


def test_statement_C():
    dag = Statement('=', 'a', 'b')
    printer = CCodePrinter(dag)
    assert(printer.code_str() == "a = b;\n")


def test_sum_of_squares_C():
    """Test for C compiling \sum_{i=1}^N i*i"""
    dag = create_sum_squares()
    cp = CCodePrinter(dag)
    module_name = "ignition_sum_of_squares_c"
    module_path = cp.to_ctypes_module(module_name)
    sys.path.append(module_path)
    sum_of_squares = import_module(module_name)
    assert(sum_of_squares.sum_squares(4) == 30)


def test_double_sum_C():
    dag = create_double_sum()
    modname = "ignition_double_sum_c"
    modpath = CCodePrinter(dag).to_ctypes_module(modname)
    sys.path.append(modpath)
    double_sum = import_module(modname)
    assert(double_sum.double_sum(3) == 20)


def test_index_variable_loop_C():
    dag = create_index_variable_loop()
    modname = "ignition_index_variable_loop_c"
    modpath = CCodePrinter(dag).to_ctypes_module(modname)
    sys.path.append(modpath)
    index_variable_loop = import_module(modname)
    assert(index_variable_loop.idx_loop_fun() == 45)


def test_statement_Py():
    dag = Statement("=", 'a', 'b')
    printer = PythonCodePrinter(dag)
    assert(printer.code_str() == "a = b\n")


def test_sum_of_squares_Py():
    """Test for Python running \sum_{i=1}^N i*i"""
    dag = create_sum_squares()
    cp = PythonCodePrinter(dag)
    module_name = "ignition_sum_of_squares_py"
    module_path = cp.to_module(module_name)
    sys.path.append(module_path)
    sum_of_squares = import_module(module_name)
    assert(sum_of_squares.sum_squares(4) == 30)


def test_double_sum_Py():
    dag = create_double_sum()
    modname = "ignition_double_sum_py"
    modpath = PythonCodePrinter(dag).to_module(modname)
    sys.path.append(modpath)
    double_sum = import_module(modname)
    assert(double_sum.double_sum(3) == 20)


def test_class_Py():
    dag = create_class_obj()
    modname= "ignition_class_obj_py"
    modpath = PythonCodePrinter(dag).to_module(modname)
    sys.path.append(modpath)
    ignition_class_obj = import_module(modname)
    counter = ignition_class_obj.Counter()
    assert(counter.count == 0)
    counter.add_one()
    assert(counter.count == 1)
