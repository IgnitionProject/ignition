#ifndef __EX1__
#define __EX1__

#include <math.h>

const unsigned int NUM_QUAD_PTS = 5;
const double QUAD_PTS[5] = {-0.906179845939, -0.538469310106, 0.0, 0.538469310106, 0.906179845939};
const double QUAD_WTS[5] = {0.236926885056, 0.478628670499, 0.568888888889, 0.478628670499, 0.236926885056};

double eval_gen(double* u)
{
  double ret_val = 0.0;
  ret_val += 0.459697694131860;

  ret_val += 0.118333123748775*(u[0])
           + 0.232970501924733*(u[1])
           + 0.249623484271039*(u[2])
           + 0.171933767086186*(u[3])
           + 0.0686101077775073*(u[4]);
  return ret_val;
}

#endif /* __EX1__ */
