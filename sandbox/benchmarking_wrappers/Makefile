PYTHONINC=/Users/aterrel/workspace/opt/apps/anaconda/1.4.0/include/python2.7
PYTHONLIB=/Users/aterrel/workspace/opt/apps/anaconda/1.4.0/lib
SHARED_OBJS=libsum_of_squares.so sum_of_squares_cython.so
CYTHON_INTERMEDIATE=sum_of_squares_cython.c
BENCH_EXEC=benchmark.py
TARGETS= $(BENCH_EXEC) $(SHARED_OBJS) sum_of_squares_ctypes.py

CC=gcc
CYTHON=cython
PYTHON=python

CFLAGS=-I $(PYTHONINC) -O2 -Wall -fwrapv -fno-strict-aliasing -std=gnu99
LDFLAGS=-fPIC -shared 
PYLDFLAGS=-pthread -L $(PYTHONLIB) -Wl,-rpath,$(PYTHONLIB) -lpython2.7 -L . -lsum_of_squares

bench: $(TARGETS)
	$(PYTHON) $<

libsum_of_squares.so: sum_of_squares.c sum_of_squares.h
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

sum_of_squares_cython.c:sum_of_squares_cython.pyx libsum_of_squares.so csum_of_squares.pxd
	$(CYTHON) $<

sum_of_squares_cython.so:sum_of_squares_cython.c
	$(CC) $(CFLAGS) $(LDFLAGS) $(PYLDFLAGS) -o $@ $<

clean: 
	$(RM) -rf $(SHARED_OBJS) $(CYTHON_INTERMEDIATE) *.pyc
