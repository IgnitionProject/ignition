from cffi import FFI

ffi = FFI()
ffi.cdef("""int sum_of_squares(int N);""")

C = ffi.dlopen("./libsum_of_squares.so")

def sum_of_squares_cffi(N):
    arg = ffi.cast("int", N)
    return C.sum_of_squares(arg)
