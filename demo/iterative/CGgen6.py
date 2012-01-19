#!/usr/bin/env python

from pme import *

ind = "    "
if __name__== "__main__":
    pme = PME()
    A = Smatrix(1,1); A.setscalar("A")
    pme.addvar("A",1,1,argsrc="Input")
    R = Smatrix(1,3); R.setfull("R")
    pme.addvar("R",1,3,argsrc="Overwrite")
    P = Smatrix(1,3); P.setfull("P")
    pme.addvar("P",1,3)
    D = Smatrix(3,3); D.setscalar("D")
    pme.addvar("D",3,3,prefix="Diag_")
    I = Smatrix(3,3); I.setI()
    pme.addvar("I",3,3,prefix="I_")
    J = Smatrix(3,3); J.setJ()
    pme.addvar("J",3,3,prefix="J_")
    JI = Smatrix(3,3); JI.setlowerbi("JI");
    pme.addvar("JI",3,3)
    pme.append( I-J-JI, threecol )
    pme.append( R*J-R*I-A*P*D, threenull )
    pme.append( R*JI-A*P*D, threenull )
    U = Smatrix(3,3); U.setstrictupper("U")
    pme.addvar("U",3,3,"Upper_")
    pme.append( P*I-P*U-R, threeline )
    W = Smatrix(3,3); W.setscalar("W")
    pme.addvar("W",3,3,"Diag_")
    Z = Smatrix(3,3); Z.setscalar("Z")
    pme.addvar("Z",3,3,"Diag_")
    pme.append( R.t()*R-W, threediag )
    pme.append( P.t()*A*P-Z, threediag )
    print "\nGoing to try",pme.length(),"sets"
    c = 1
    for eqns in pme.invariants():
        print "\n****************************************************************\n\n"
        print "Invariant",c # ,":",eqns
        fn = "CG"+str(c)+".py"
        f = open("cgauto/"+fn,'w')
        pme.printhead(f=f,c=c)
        for v in pme.vars:
            f.write( ind+"%s = %s\n" % ( str(v.object),v.name ) )
        # take apart the objects
        f.write(ind+"eqns = [\n")
        for e in eqns:
            f.write(ind+" "+e+" ,\n")
        f.write(ind+"]\n")
        #
        pme.printtail(f=f,c=c)
        f.close()
        oname = "alg"+str(c)+".in"
        command = "cd cgauto; python %s > /dev/null 2>&1 ; if [ -f %s ] ; then if [ `cat %s | wc -l ` -gt 3 ] ; then echo 'solutions' ; make alg -f ../Makefile N=%d ; fi ; fi" % \
                  (fn,oname,oname,c)
        #print "Command:",command
        os.system(command)
        c += 1
        if c>100: break
