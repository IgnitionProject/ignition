PYTHON_PREFIX=$(shell python2.7-config --prefix)
PYTHON_LIB=$(PYTHON_PREFIX)/lib
SHARED_OBJS=libsum_of_squares.so sum_of_squares_swig.o _sum_of_squares_swig.so sum_of_squares_cython.so sum_of_squares_extension.so sum_of_squares_bitey.o
CYTHON_INTERMEDIATE=sum_of_squares_cython.c
SWIG_INTERMEDIATE=sum_of_squares_swig_wrap.c sum_of_squares_swig.py sum_of_squares_swig_wrap.o
BENCH_EXEC=benchmark.py
TARGETS= $(BENCH_EXEC) $(SHARED_OBJS) sum_of_squares_ctypes.py 

CC=gcc
CYTHON=cython
PYTHON=python
SWIG=swig -python
CLANG=clang

CFLAGS=-O2 -std=gnu99 -fPIC 
LDFLAGS=-shared
PY_CFLAGS=$(shell python2.7-config --cflags)
PY_LDFLAGS=-L$(PYTHON_LIB) -Wl,-rpath,$(PYTHON_LIB) $(shell python2.7-config --ldflags)
SQUARES_LDFLAGS=-L. -Wl,-rpath,$(PWD) -lsum_of_squares

bench: $(TARGETS)
	$(PYTHON) $<

libsum_of_squares.so: sum_of_squares.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

sum_of_squares_cython.c:sum_of_squares_cython.pyx libsum_of_squares.so csum_of_squares.pxd
	$(CYTHON) $<

sum_of_squares_cython.so:sum_of_squares_cython.c
	$(CC) $(CFLAGS) $(PY_CFLAGS) $(LDFLAGS) $(PY_LDFLAGS) $(SQUARES_LDFLAGS) -o $@ $<

sum_of_squares_swig_wrap.c:sum_of_squares_swig.i
	$(SWIG) $<

sum_of_squares_swig_wrap.o:sum_of_squares_swig_wrap.c
	$(CC) $(CFLAGS) $(PY_CFLAGS) -c $<

_sum_of_squares_swig.so: sum_of_squares_swig_wrap.o sum_of_squares_swig.o
	$(CC) $(CFLAGS) $(PY_CFLAGS) $(LDFLAGS) $(PY_LDFLAGS) $(SQUARES_LDFLAGS) -o $@ $^

sum_of_squares_extension.so: sum_of_squares_extension.c
	$(CC) $(CFLAGS) $(PY_CFLAGS) $(LDFLAGS) $(PY_LDFLAGS) $(SQUARES_LDFLAGS) -o $@ $<

sum_of_squares_bitey.o: sum_of_squares_bitey.c
	$(CLANG) -emit-llvm -c $<

clean: 
	$(RM) -rf $(SHARED_OBJS) $(CYTHON_INTERMEDIATE) $(SWIG_INTERMEDIATE) *.pyc *.dSYM
