import copy
import itertools
import os
import re

def minus(op):
    if op==" - ":
        return " + "
    else: return " - "
def stradd(a,b):
    at = a.split("_")[0]; bt = b.split("_")[0]
    op = " + "
    if a[0]=="-":
        a = a[1:]; op = minus(op)
    if b[0]=="-":
        b = b[1:]; op = minus(op)
    if at=="0": return b
    elif bt=="0": return a
    else: return a+op+b
def strsub(a,b):
    at = a.split("_")[0]; bt = b.split("_")[0]
    if at=="0": return b
    elif bt=="0": return a
    else: return a+" - "+b
def strmul(a,b):
    at = a.split("_")[0]; bt = b.split("_")[0]
    if at=="0" or bt=="0": return "0"
    elif at=="1" or at=="I": return b
    elif bt=="1" or bt=="I": return a
    elif at=="-1" or at=="-I": return "-"+b
    elif bt=="-1" or bt=="-I": return "-"+a
    else: return a+" * "+b

class Smatrix():
    def __init__(self,isize,jsize):
        self.isize = isize; self.jsize = jsize
        self.array = [ [ "0" for j in range(jsize) ] for i in range(isize) ]
        if isize>1:
            self.vletters = [ "m" for i in range(self.isize) ]
            self.vletters[0] = "t"; self.vletters[self.isize-1] = "b"
        else: self.vletters = [ "" for i in range(self.isize) ]
        if jsize>1:
            self.hletters = [ "m" for j in range(self.jsize) ]
            self.hletters[0] = "l"; self.hletters[self.jsize-1] = "r"
        else: self.hletters = [ "" for j in range(self.jsize) ]
    def __getitem__(self,idx):
        if idx[0]<0 or idx[0]>=len(self.array):
            print "ERROR i index %d out of range %d" % \
                  (idx[0],len(self.array)-1)
        if idx[1]<0 or idx[1]>=len(self.array[idx[0]]):
            print "ERROR j index %d out of range %d" % \
                  (idx[1],len(self.array[idx[0]])-1)
        return self.array[idx[0]][idx[1]]
    def __setitem__(self,idx,val):
        self.array[idx[0]][idx[1]] = val
    def multisub(self,iset):
        #print "multisub of",self,"by",iset
        s = []
        for i in iset:
            s.append(self[(i)])
        return s
    def setscalar(self,value):
        for k in range(self.isize):
            self[(k,k)] = value
        self.annotated()
    def setfull(self,value):
        for i in range(self.isize):
            for j in range(self.jsize):
                self[(i,j)] = value
        self.annotate()
    def setupper(self,value):
        for i in range(self.isize):
            for j in range(self.jsize):
                if j>=i: self[(i,j)] = value
        self.annotate()
    def setunitupper(self,value):
        for i in range(self.isize):
            for j in range(self.jsize):
                if j>=i:
                    if j==i and i>0 and i<self.isize-1:
                        self[(i,j)] = "I"
                    else: self[(i,j)] = value
        self.annotate()
    def setstrictupper(self,value):
        for i in range(self.isize):
            for j in range(self.jsize):
                if j>=i:
                    if j==i and i>0 and i<self.isize-1:
                        self[(i,j)] = "0"
                    else: self[(i,j)] = value
        self.annotate()
    def setlower(self,value):
        for i in range(self.isize):
            for j in range(self.jsize):
                if j<=i: self[(i,j)] = value
        self.annotate()
    def setlowerbi(self,value):
        for i in range(self.isize):
            for j in range(self.jsize):
                if j==i or j==i-1: self[(i,j)] = value
        self.annotate()
    def setI(self):
        for i in range(self.isize):
            for j in range(self.jsize):
                if j==i:
                    self[(i,j)] = "I"
        self.annotate()
    def setJ(self):
        for i in range(self.isize):
            for j in range(self.jsize):
                if j==i:
                    if i==0 or i==self.isize-1: self[(i,j)] = "J"
                elif i==j+1: self[(i,j)] = "j"
        self.annotate()
    def annotate(self):
        for i in range(self.isize):
            for j in range(self.jsize):
                e = self[(i,j)]; x = self.vletters[i]+self.hletters[j]
                if e!="0" and e!="I" and x!="":
                    self[(i,j)] = e+"_"+x
    def annotated(self):
        for i in range(self.isize):
            for j in range(self.jsize):
                e = self[(i,j)]; x = self.hletters[j]
                if e!="0" and e!="I" and x!="":
                    self[(i,j)] = e+"_"+x
    def __repr__(self):
        return repr(self.array)
    def t(self):
        r = Smatrix(self.jsize,self.isize)
        for i in range(self.isize):
            for j in range(self.jsize):
                r[(j,i)] = "T("+self[(i,j)]+")"
        return r
    def __add__(self,other):
        if self.isize!=other.isize or self.jsize!=other.jsize:
            print "Incompatible matrices"; return 0
        r = Smatrix(self.isize,self.jsize)
        for i in range(self.isize):
            for j in range(self.jsize):
                r[(i,j)] = stradd( self[(i,j)], other[(i,j)] )
        return r
    def __sub__(self,other):
        if self.isize!=other.isize or self.jsize!=other.jsize:
            print "Incompatible matrices"; return 0
        r = Smatrix(self.isize,self.jsize)
        for i in range(self.isize):
            for j in range(self.jsize):
                r[(i,j)] = strsub( self[(i,j)], other[(i,j)] )
        return r
    def __mul__(self,other):
        M = self.isize; N = other.jsize; K1 = self.jsize; K2 = other.isize
        if K1!=K2:
            print "Incompatible matrices (%d,%d) (%d,%d)" % ( M,K1,K2,N); return 0
        r = Smatrix(M,N)
        for i in range(M):
            for j in range(N):
                r[ (i,j) ] = strmul( self[(i,0)], other[(0,j)] )
        for k in range(1,K1):
            for i in range(M):
                for j in range(N):
                    r[ (i,j) ]  = stradd( r[(i,j)],
                                          strmul( self[(i,k)], other[(k,j)] ) )
        return r
    def eqns(self,irange,jrange):
        for i in range(min(self.isize,irange)):
            for j in range(min(self.jsize,jrange)):
                yield self[(i,j)]


threesets = [ [ [0,0] ],
              [ [0,0], [0,1] ],
              [ [0,0], [1,0] ],
              [ [0,0], [0,1], [1,0], [1,1] ],
              ]
threediag = [ [ [0,0] ],
              [ [0,0], [0,1], [1,0] ],
              [ [0,0], [0,1], [1,0], [1,1] ],
              ]
threeline = [ [ [0,0] ],
              [ [0,0], [0,1] ],
              ]
threenull = [[[ 0,0 ]]]

class PME():
    def __init__(self):
        self.exprs = []
        self.invar = []
    def append(self,expr,invar=None):
        self.exprs.append(expr)
        if invar is None:
            self.invar.append( threesets )
        else: self.invar.append( invar )
    def length(self):
        c = 1
        for p in itertools.product( *self.invar ):
            c += 1
        return c
    def invariants(self):
        for p in itertools.product( *self.invar ):
            eqns = []
            for i in range(len(p)):
                for s in self.exprs[i].multisub(p[i]):
                    eqns.append(s)
            yield eqns
            
