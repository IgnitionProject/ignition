cimport csum_of_squares

def sum_of_squares_cython_wrap(int N):
    return csum_of_squares.sum_of_squares(N)

def sum_of_squares_cython_compile(int N):
    cdef int sum = 0
    cdef int i
    for i in range(1, N+1):
        sum += i*i
    return sum
