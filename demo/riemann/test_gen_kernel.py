import numpy

def kernel(q_l, q_r, consts):
    K, rho = consts
    A = numpy.matrix([[    0, K],
                      [1/rho, 0]])
    evals, v1 = numpy.linalg.eig(A)
    _, v2 = numpy.linalg.eig(A.transpose())
    lam = numpy.diag(evals)
    L = v1
    R = v2.transpose()


    alpha = L*(q_r - q_l)
    w = alpha.transpose()*R
    w = w.transpose()
    s = numpy.diag(lam)
    lam_neg = lam.copy()
    lam_pos = lam.copy()
    for m in xrange(lam_neg.shape[0]):
            if lam_neg[m,m] > 0.0:
                lam_neg[m,m] = 0.0
            if lam_pos[m,m] < 0.0:
                lam_pos[m,m] = 0.0
    # print lam_neg
    # print w
    # print lam_neg * w.transpose()
    amdq = lam_neg*w
    apdq = lam_pos*w
    print "L", L
    print "R", R
    print "A", A
    print "L*lam*R", L*lam*R
    print "lam_neg", lam_neg
    print "lam_pos", lam_pos
    return w, s, amdq, apdq

def main():
#    q_l = numpy.zeros([2,1], dtype=numpy.float)
#    q_r = numpy.ones([2,1], dtype=numpy.float)
    q_l = numpy.matrix([[0.], [1.]])
    q_r = numpy.matrix([[0.], [0.]])
    consts = (1.0, 4.0)
    w, s, amdq, apdq = kernel(q_l, q_r, consts)
    print "W", w
    print "S", s
    print "AMDQ", amdq
    print "APDQ", apdq

#if __name__ == "__main":
main()
