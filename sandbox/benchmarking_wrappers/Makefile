PYTHON_PREFIX=$(shell python2.7-config --prefix)
PYTHON_LIB=$(PYTHON_PREFIX)/lib
SHARED_OBJS=libsum_of_squares.so sum_of_squares.o _sum_of_squares.so sum_of_squares_cython.so sum_of_squares_cython.so.dSYM
CYTHON_INTERMEDIATE=sum_of_squares_cython.c
SWIG_INTERMEDIATE=sum_of_squares_wrap.c sum_of_squares.py sum_of_squares_wrap.o
BENCH_EXEC=benchmark.py
TARGETS= $(BENCH_EXEC) $(SHARED_OBJS) sum_of_squares_ctypes.py 

CC=gcc
CYTHON=cython
PYTHON=python
SWIG=swig -python

CFLAGS=-O2 -std=gnu99
LDFLAGS=-fPIC -shared
PY_CFLAGS=$(shell python2.7-config --cflags)
PY_LDFLAGS=-L$(PYTHON_LIB) -Wl,-rpath,$(PYTHON_LIB) $(shell python2.7-config --ldflags)
SQUARES_LDFLAGS=-L. -Wl,-rpath,$(PWD) -lsum_of_squares

bench: $(TARGETS)
	$(PYTHON) $<

sum_of_squares.o: sum_of_squares.c sum_of_squares.h
	$(CC) $(CFLAGS) -c $<

libsum_of_squares.so: sum_of_squares.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

sum_of_squares_cython.c:sum_of_squares_cython.pyx libsum_of_squares.so csum_of_squares.pxd
	$(CYTHON) $<

sum_of_squares_cython.so:sum_of_squares_cython.c
	$(CC) $(CFLAGS) $(PY_CFLAGS) $(LDFLAGS) $(PY_LDFLAGS) $(SQUARES_LDFLAGS) -o $@ $<
	install_name_tool -change /opt/anaconda1anaconda2anaconda3/lib/libpython2.7.dylib /Users/aterrel/workspace/opt/apps/anaconda/1.4.0/lib/libpython2.7.dylib $@

sum_of_squares_wrap.c:sum_of_squares.i
	$(SWIG) $<

sum_of_squares_wrap.o:sum_of_squares_wrap.c
	$(CC) $(CFLAGS) $(PY_CFLAGS) -c $<
	install_name_tool -change /opt/anaconda1anaconda2anaconda3/lib/libpython2.7.dylib /Users/aterrel/workspace/opt/apps/anaconda/1.4.0/lib/libpython2.7.dylib $@

_sum_of_squares.so: sum_of_squares_wrap.o libsum_of_squares.so
	$(CC) $(CFLAGS) $(PY_CFLAGS) $(LDFLAGS) $(PY_LDFLAGS) $(SQUARES_LDFLAGS) -o $@ $<
	install_name_tool -change /opt/anaconda1anaconda2anaconda3/lib/libpython2.7.dylib /Users/aterrel/workspace/opt/apps/anaconda/1.4.0/lib/libpython2.7.dylib $@

clean: 
	$(RM) -rf $(SHARED_OBJS) $(CYTHON_INTERMEDIATE) $(SWIG_INTERMEDIATE) *.pyc
