import numpy as np

# define data stack
x = np.array([[2, -1, 3], [-1, 3, 5], [0, 2, 4], [4, -2, -1], [1, 0, 4], [-2, 5, 5]])

# calculate mean in each dimension
x_mean = np.mean(x, axis=0)

# center the data
x_centered = x - x_mean

# get U, S and Vh
U, S, Vh = np.linalg.svd(x_centered)

# get the reuslt of PCA as a series of terms and print each term
result = np.zeros(x.shape)
for i in range(len(S)):
    term = S[i] * np.outer(U[:, i], Vh[i, :])
    print("term" + str(i) + ":\n" + str(term))
    result += term

# print the result
print("result:\n" + str(result))
print("main principal component is: " + str(Vh[0, :]) + " with eigenvalue " + str(S[0]))
print("second principal component is: " + str(Vh[1, :]) + " with eigenvalue " + str(S[1]))
print("third principal component is: " + str(Vh[2, :]) + " with eigenvalue " + str(S[2]))

# equation of regression line in 3D (with main principal component)
# y = x_mean + c * Vh[0, :]
print("equation of regression line: y = " + str(x_mean) + " + c * " + str(S[0]) + " * " + str(Vh[0, :]))

# equation of regression plane
# y = x_mean + c_1 * Vh[0, :] + c_2 * Vh[1, :]
print("equation of regression plane: y = " + str(x_mean) + " + c_1 * " + str(S[0]) + " * " + str(Vh[0, :]) + " + c_2 * " + str(S[1]) + " * " + str(Vh[1, :]))

# term0:
# [[ 1.26777985 -1.49808671 -1.2214064 ]
#  [-1.63595742  1.93314798  1.5761166 ]
#  [-0.68992695  0.81526015  0.66469048]
#  [ 3.38398889 -3.99872956 -3.26020776]
#  [ 0.32174938 -0.38019888 -0.30998028]
#  [-2.64763375  3.12860701  2.55078736]]
# term1:
# [[ 3.24500178e-02 -6.86281010e-01  8.75423554e-01]
#  [ 3.84594342e-03 -8.13373339e-02  1.03754318e-01]
#  [-2.59895606e-04  5.49649681e-03 -7.01135934e-03]
#  [-3.96221134e-02  8.37962684e-01 -1.06890947e+00]
#  [ 3.65558568e-02 -7.73114841e-01  9.86189231e-01]
#  [-3.29698090e-02  6.97274004e-01 -8.89446273e-01]]
# term2:
# [[ 0.03310347  0.01770105  0.01264952]
#  [-0.03455519 -0.01847731 -0.01320425]
#  [ 0.02352018  0.01257668  0.00898755]
#  [-0.01103344 -0.00589979 -0.00421611]
#  [-0.02497191 -0.01335295 -0.00954228]
#  [ 0.01393689  0.00745232  0.00532557]]
# result:
# [[ 1.33333333 -2.16666667 -0.33333333]
#  [-1.66666667  1.83333333  1.66666667]
#  [-0.66666667  0.83333333  0.66666667]
#  [ 3.33333333 -3.16666667 -4.33333333]
#  [ 0.33333333 -1.16666667  0.66666667]
#  [-2.66666667  3.83333333  1.66666667]]
# main principal component is: [-0.54844932  0.64808147  0.52838788] with eigenvalue 8.805815341737175
# second principal component is: [ 0.02915978 -0.61669628  0.78666092] with eigenvalue 2.4397130178629425
# third principal component is: [-0.83567521 -0.44685132 -0.31932874] with eigenvalue 0.07359726690803713
# equation of regression line: y = [0.66666667 1.16666667 3.33333333] + c * 8.805815341737175 * [-0.54844932  0.64808147  0.52838788]
# equation of regression plane: y = [0.66666667 1.16666667 3.33333333] + c_1 * 8.805815341737175 * [-0.54844932  0.64808147  0.52838788] + c_2 * 2.4397130178629425 * [ 0.02915978 -0.61669628  0.78666092]