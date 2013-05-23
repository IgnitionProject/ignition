
from ctypes import cdll

sum_lib = cdll.LoadLibrary('./libsum_of_squares.so')

def sum_of_squares_ctypes(N):
    return sum_lib.sum_of_squares(N)
