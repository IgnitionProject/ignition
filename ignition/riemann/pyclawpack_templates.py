numerical_eigen_decomp = """A = %s
eigen_vals, R = np.linalg.eig(A)
Rinv = np.linalg.inv(R)
lam = np.diag(eigen_vals)
"""

pointwise_kernel = """alpha = Rinv*(q_r - q_l)
w = np.diag(np.ravel(alpha))*R
lam_neg = np.diag(map(lambda x: 0.0 if x > -1e-10 else x, eigen_vals))
lam_pos = np.diag(map(lambda x: 0.0 if x < 1e-10 else x, eigen_vals))
amdq = w*lam_neg 
apdq = w*lam_pos
"""

func_decl = """def kernel(q_l, q_r, aux_l, aux_r, aux_global):
"""

func_return = """return wave, s, amdq, apdq
"""
