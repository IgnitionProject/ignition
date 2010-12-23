#include <stdio.h>
#include <math.h>
#include <sys/time.h>
#include "ex1.h"


double gtod_ref_time_sec = 0.0;
double dclock()
{
  double the_time, norm_sec;
  struct timeval tv;

  gettimeofday( &tv, NULL );
  the_time = tv.tv_usec*1.0e-6;

  /* // If this is the first invocation of through dclock(), */
  /* // then initialize the "reference time" global variable */
  /* // to the seconds field of the tv struct. */
  /* if( gtod_ref_time_sec == 0.0 ) */
  /*   gtod_ref_time_sec = ( double ) tv.tv_sec; */

  /* // Normalize the seconds field of the tv struct so that */
  /* // it is relative to the "reference time" that was recorded */
  /* // during the first invocation of dclock(). */
  /* norm_sec = ( double ) tv.tv_sec - gtod_ref_time_sec; */

  /* // Compute the number of seconds since the reference time. */
  /* the_time = norm_sec + tv.tv_usec * 1.0e-6; */

  return the_time;
}

#define NREPEATS 10
#define INNER 10000

const double MY_QUAD_PTS[2] = {-0.577350269189626, 0.577350269189626};
const double MY_QUAD_WTS[2] = {1.0, 1.0};
const int MY_NUM_QUAD_PTS = 2;

inline double x_sqr(const double val){
  return val*val;
}

inline double eval(const double* u)
{
  double sum = 0.0;
  int i;
  for(i = 0; i < NUM_QUAD_PTS; ++i){
    sum +=  QUAD_WTS[i]*(cos(0.5*QUAD_PTS[i] + 0.5)*u[i]
                           + sin(0.5*QUAD_PTS[i]+0.5));
  }
  return 0.5*sum;
}

int main()
{
  int i, j, rep;
  double time_eval, time_opt, time_gen;
  double u[NUM_QUAD_PTS];

  // u = x
  for(i=0; i< NUM_QUAD_PTS; ++i)
    u[i] = 0.5*QUAD_PTS[i] + 0.5;

  /* Time the simple implementation */
  double val[NREPEATS*INNER]; //store returned val so not optimized away
  double dtime, dtime_best;
  for ( rep=0; rep<NREPEATS; ++rep ){
    dtime = dclock();
    for (j=0; j<INNER; j++)
      val[rep*INNER+j] = eval(u);
    dtime = dclock() - dtime;
    if ( rep==0 )
      dtime_best = dtime;
    else
      dtime_best = ( dtime < dtime_best ? dtime : dtime_best );
  }
  time_eval = dtime_best;
  for ( rep=0; rep<NREPEATS*INNER; ++rep){
    if (rep % INNER == 0)
      printf("val[%d] = %f\n", rep, val[rep]);
  }


  /* Time the generated implementation */
  for ( rep=0; rep<NREPEATS; ++rep ){
    dtime = dclock();
    for (j=0; j<INNER; j++)
      val[rep*INNER+j] = eval_gen(u);
    dtime = dclock() - dtime;
    if ( rep==0 )
      dtime_best = dtime;
    else
      dtime_best = ( dtime < dtime_best ? dtime : dtime_best );
  }
  time_gen = dtime_best;
  for ( rep=0; rep<NREPEATS*INNER; ++rep){
    if (rep % INNER == 0)
      printf("val[%d] = %f\n", rep, val[rep]);
  }

  printf("time_eval: %.9f\ntime_gen:%.9f\n",
         time_eval, time_gen);
}

