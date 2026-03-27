import numpy as np
import matplotlib.pyplot as plt

# 1. Prepare the basis vectors for n = 0 to 12
n = np.arange(0, 13)
basis = [
    np.ones_like(n).astype(np.float64), # n^0
    n.astype(np.float64),              # n^1
    (n**2).astype(np.float64),         # n^2
    (n**3).astype(np.float64),         # n^3
    (n**4).astype(np.float64)          # n^4
]

ortho_basis = []

# Gram-Schmidt Orthonormalization

# find the unit vector of the first basis vector and make it the first vector in ortho_basis
ortho_basis.append(basis[0] / np.linalg.norm(basis[0]))

# project and subtract the projections of the previous orthogonal basis vectors from the current basis vector
# find the remaining orthogonal basis vectors and find the unit vector of it, then add it to ortho_basis
for i in range(1, len(basis)):
    u = basis[i].copy()
    for j in range(i):
        u -= np.dot(basis[i], ortho_basis[j]) * ortho_basis[j]   
    norm_u = np.linalg.norm(u)
    if norm_u > 1e-10:
        ortho_basis.append(u / norm_u)

# print the orthogonal basis vectors
for i in range(len(ortho_basis)):
    print("ortho_basis[" + str(i) + "]: " + str(ortho_basis[i]))


# re-construct each basis vector with the orthogonal basis vectors
# n^0 = c_0 * ortho_basis[0] + c_1 * ortho_basis[1] + c_2 * ortho_basis[2] + c_3 * ortho_basis[3] + c_4 * ortho_basis[4]
for i in range(len(basis)):
    c = [np.dot(basis[i], ortho_basis[j]) for j in range(len(ortho_basis))]
    reconstructed = np.dot(c, ortho_basis)
    error = np.linalg.norm(basis[i] - reconstructed)
    # reconstruction result should be same as basis
    # express as c_0 * ortho_basis[0] + c_1 * ortho_basis[1] + c_2 * ortho_basis[2] + c_3 * ortho_basis[3] + c_4 * ortho_basis[4]
    print("Basis n^" + str(i) + " reconstruction result: ")
    for j in range(len(ortho_basis)):
        print(str(c[j]) + " * " + str(ortho_basis[j]))
    print(" = " + str(reconstructed))
    # print the error
    print("Error: ", error)


# Create the target function
f = 1.0 / (n + 1.0)

# Project f onto the orthonormal vectors
c_f = [np.dot(f, v) for v in ortho_basis]
f_approx = np.dot(c_f, ortho_basis)

# Plot!
plt.plot(n, f, 'ro', label="Original f(n)")
plt.plot(n, f_approx, 'b-', label="4th Degree Fit")
plt.legend(); plt.savefig("exercise/DISP_4/gram_schmidt_fit.png")

