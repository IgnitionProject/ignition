#ifndef __EX1__
#define __EX1__

#include <math.h>

const unsigned int NUM_QUAD_PTS = 2;
const double QUAD_PTS[2] = {-0.57735026919, 0.57735026919};
const double QUAD_WTS[2] = {1.0, 1.0};

double eval_gen(double* u)
{
  double ret_val = 0.0;
  ret_val += 0.459697694131860;

  ret_val += 0.488876937571022*(u[0])
           + 0.352392910067197*(u[1]);
  return ret_val;
}

#endif /* __EX1__ */
