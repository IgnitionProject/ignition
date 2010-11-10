import os
from subprocess import Popen, PIPE
import sympy


from int_gen.language import *
from int_gen.generator import *

def test_symbolic_fun():
    x = sympy.Symbol("x")
    intgrl = Func(sympy.cos(x), x) * Dom(x, 0, 1)
    code = int_gen(intgrl, "tmp1", [])
    correct_code = """double tmp1()
{
  double ret_val = 0.0;
  ret_val += 0.841470984807897;
  return ret_val;
}

"""
    assert(code == correct_code)

def test_disc_fun():
    intgrl = DiscFunc("u") * Dom("x", 0, 1)
    code = int_gen(intgrl, "tmp1", ["u"])
    correct_code = """double tmp1(double* u)
{
  double ret_val = 0.0;

  unsigned int i;
  for (i=0; i<NUM_QUAD_PTS; ++i)
    ret_val += 0.500000*QUAD_WTS[i]*(u[i]);
  return ret_val;
}

"""
    assert(code == correct_code)

def test_add_fun():
    x = sympy.Symbol("x")
    intgrl = (DiscFunc("u") + Func(sympy.cos(x), x)) * Dom("x", 0, 1)
    code = int_gen(intgrl, "tmp1", ["u"])
    correct_code = """double tmp1(double* u)
{
  double ret_val = 0.0;
  ret_val += 0.841470984807897;

  unsigned int i;
  for (i=0; i<NUM_QUAD_PTS; ++i)
    ret_val += 0.500000*QUAD_WTS[i]*(u[i]);
  return ret_val;
}

"""
    assert(code == correct_code)

def test_mul_fun():
    x = sympy.Symbol("x")
    intgrl = (DiscFunc("u") * Func(sympy.cos(x), x)) * Dom("x", 0, 1)
    code = int_gen(intgrl, "tmp1", ["u"])
    correct_code = """double tmp1(double* u)
{
  double ret_val = 0.0;

  unsigned int i;
  for (i=0; i<NUM_QUAD_PTS; ++i)
    ret_val += 0.500000*QUAD_WTS[i]*(u[i]*cos((0.500000*QUAD_PTS[i]+0.500000)));
  return ret_val;
}

"""
    assert(code == correct_code)

def test_complex_fun():
    x = sympy.Symbol("x")
    u = DiscFunc("u")
    v = DiscFunc("v")
    eqn = u * v + Func(sympy.cos(x), x) * u * v + Func(sympy.cos(x) * x ** 2, x)
    intgrl = eqn * Dom("x", 0, 1)
    code = int_gen(intgrl, "tmp1", ["u", "v"])
    correct_code = """double tmp1(double* u, double* v)
{
  double ret_val = 0.0;
  ret_val += 0.239133626928383;

  unsigned int i;
  for (i=0; i<NUM_QUAD_PTS; ++i)
    ret_val += 0.500000*QUAD_WTS[i]*(u[i]*v[i]+cos((0.500000*QUAD_PTS[i]+0.500000))*u[i]*v[i]);
  return ret_val;
}

"""
    assert(code == correct_code)

def test_gen_file():
    x = sympy.Symbol("x")
    u = DiscFunc("u")
    v = DiscFunc("v")
    eqn = u * v + Func(sympy.cos(x), x) * u * v + Func(sympy.cos(x) * x ** 2, x)
    intgrl = eqn * Dom("x", 0, 1)
    os.mkdir("test_tmp")
    os.chdir("test_tmp")
    gen_file("tmp_gen_file", [intgrl], ["tmp"], [["u", "v"]])
    test_file = open("test.c", 'w')
    test_file.write("""
#include <stdio.h>
#include "tmp_gen_file.h"

int main()
{
  double u[5] = {1.0, 1.0, 1.0, 1.0, 1.0};
  double v[5] = {2.0, 2.0, 2.0, 2.0, 2.0};
  printf("%.9f\\n", tmp(u, v));
}    
    """)
    test_file.close()
    output = Popen(["gcc", "test.c"], stdout=PIPE).communicate()[0]
    if output: print "From gcc:", output
    output = Popen(["./a.out"], stdout=PIPE).communicate()[0]
    if output: print "From a.out:", output
    pass_test = abs(float(output) - 3.92207559654418) < 10e-6
    if pass_test:
        for f in os.listdir("."):
            os.remove(f)
        os.chdir("..")
        os.rmdir("test_tmp")
    else:
        os.chdir("..")
        print("Left generated files in test_tmp.")
        assert(False)
