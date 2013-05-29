#include <Python.h>
#include "sum_of_squares.h"

static PyObject *
sum_of_squares_extension_sum_of_squares_extension(PyObject *self, PyObject *args)
{
  const int N;
  int ret_val;

  if (!PyArg_ParseTuple(args, "i", &N))
    return NULL;
  ret_val = sum_of_squares(N);
  return Py_BuildValue("i", ret_val);
}

static PyMethodDef SumOfSquaresExtensionMethods[] = {
  {"sum_of_squares_extension", sum_of_squares_extension_sum_of_squares_extension, METH_VARARGS,
   "sum squares from 1 to N."},
  {NULL, NULL, 0, NULL} /* Sentinel */
};

PyMODINIT_FUNC
initsum_of_squares_extension(void)
{
  (void) Py_InitModule("sum_of_squares_extension", SumOfSquaresExtensionMethods);
}
