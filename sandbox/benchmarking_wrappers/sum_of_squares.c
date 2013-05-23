int sum_of_squares(int N) {
  int sum = 0.0;
  for(int i=1; i<N+1; ++i)
    sum += i*i;
  return sum;
}
