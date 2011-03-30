import numpy as np

def kernel(q_l, q_r, consts):


    K, rho = consts
    A = np.matrix([[    0, K],
                      [1/rho, 0]])
    evals, v1 = np.linalg.eig(A)
    _, v2 = np.linalg.eig(A.transpose())
    lam = np.diag(evals)
    L = v1
    R = v2.transpose()


    alpha = L*(q_r - q_l)
    print alpha[0,0], alpha[1,0]
    print R[:,0], R[:,1]
    print alpha[0,0]*R[:,0], alpha[1,0]*R[:,1]
    w = R*np.diag(np.ravel(alpha))
    w0 = alpha[0,0]*R[:,0]
    w1 = alpha[1,0]*R[:,1]
    print w0,
    print w1
    w[:,0] = w0
    print w
    s = evals
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

def kernel_2(q_l, q_r, consts):
    K, rho = consts

    A = np.matrix([[    0, K],
                   [1/rho, 0]])
    eigen_vals, R = np.linalg.eig(A)
    eigen_vals_2, L_t = np.linalg.eig(A.transpose())
    L = L_t.transpose()
    lam = np.diag(eigen_vals)
    print "R",  R
    print "L:", L
    print "R^-1:", np.linalg.inv(R)
    L = np.linalg.inv(R)
    print "I:", L*R
    print "eigen_vals:", eigen_vals
    print "eigen_vals_2:", eigen_vals_2
    print "L*lam*R", L*lam*R

    alpha = L*(q_r - q_l)
    w = np.diag(np.ravel(alpha))*R
    #w = R*np.diag(np.ravel(alpha))
    # w = np.matrix(np.zeros(A.shape))
    # print alpha[0,0]*R[:,0]
    # print "w", w
    # print "w[0,:]", w[0,:]
    # print "w[:,0]", w[:,0]
    # w[:,0] = alpha[0,0]*R[:,0]
    # w[:,1] = alpha[1,0]*R[:,1]
    s = eigen_vals
    lam_neg = map(lambda x: [0.0] if x > -1e-10 else [x], eigen_vals)
    lam_pos = map(lambda x: [0.0] if x < 1e-10 else [x], eigen_vals)
    print "lam_neg:", lam_neg
    print "lam_pos:", lam_pos
    amdq = np.dot(w, lam_neg)
    apdq = np.dot(w, lam_pos)
    return w, s, amdq, apdq


def main():
#    q_l = np.zeros([2,1], dtype=np.float)
#    q_r = np.ones([2,1], dtype=np.float)
    q_l = np.matrix([[0.], [0.]])
    q_r = np.matrix([[1.], [0.]])
    consts = (1.0, 4.0)
    w, s, amdq, apdq = kernel_2(q_l, q_r, consts)
    print "W", w
    print "S", s
    print "AMDQ", amdq
    print "APDQ", apdq

#if __name__ == "__main":
main()
