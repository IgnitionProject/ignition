import os
from subprocess import Popen, PIPE
import sympy


from ignition.dsl.int_gen.language import DiscFunc, Dom, Func
from ignition.dsl.int_gen.generator import gen_file, int_gen

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

  ret_val += 0.118463442528*(u[0])
           + 0.23931433525*(u[1])
           + 0.284444444444*(u[2])
           + 0.23931433525*(u[3])
           + 0.118463442528*(u[4]);
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

  ret_val += 0.118463442528*(u[0])
           + 0.23931433525*(u[1])
           + 0.284444444444*(u[2])
           + 0.23931433525*(u[3])
           + 0.118463442528*(u[4]);
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

  ret_val += 0.118333123748775*(u[0])
           + 0.232970501924733*(u[1])
           + 0.249623484271039*(u[2])
           + 0.171933767086186*(u[3])
           + 0.0686101077775073*(u[4]);
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

  ret_val += 0.118463442528*(u[0]*v[0] + 0.998899924090178*u[0]*v[0])
           + 0.23931433525*(u[1]*v[1] + 0.973491628412768*u[1]*v[1])
           + 0.284444444444*(u[2]*v[2] + 0.877582561890373*u[2]*v[2])
           + 0.23931433525*(u[3]*v[3] + 0.718443242887239*u[3]*v[3])
           + 0.118463442528*(u[4]*v[4] + 0.579166925368017*u[4]*v[4]);
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
