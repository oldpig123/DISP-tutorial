import numpy as np
import cv2
import matplotlib.pyplot as plt

# construct an elliptic image
# center of ellipse is (x_0, y_0), this is also the image center
# axis_r, axis_y are r_x, r_y
# size is (M, N)
def construct_elliptic_image(M, N, x_0, y_0, r_x, r_y):
    # center at (0, 0) first
    n_x = np.arange(0, M)
    n_y = np.arange(0, N)
    x, y = np.meshgrid(n_x, n_y)
    
    # construct the ellipse
    ellipse = ((x-x_0)/r_x)**2 + ((y-y_0)/r_y)**2 <= 1
    
    # return the ellipse
    return ellipse

# construct a elliptic image
image = construct_elliptic_image(256, 256, 64, 128, 64, 32) # image size (256, 256), center (64, 128), axis (64, 32), (0, 0) is top-left

# convert to uint8
image_output = (image * 255).astype(np.uint8)

# save the image
cv2.imwrite("exercise/DISP_5/elliptic_image.png", image_output)

# L_0 norm calculation
# count the number of non-zero pixels
L0_norm = np.sum(image != 0)
print("L0 norm: ", L0_norm)
# L_1 norm calculation
# sum of absolute values of all pixels
L_1_norm = np.sum(np.abs(image))
print("L1 norm: ", L_1_norm)
# L_2 norm calculation
# squre root of sum of squares of all pixels
L_2_norm = np.sqrt(np.sum(image**2))
print("L2 norm: ", L_2_norm)
# L_infinity norm calculation
# maximum absolute value of all pixels
L_inf_norm = int(np.max(np.abs(image)))
print("L_infinity norm: ", L_inf_norm)

# central moment calculation

# \hat{m}_{1,0} = \sum_{i=0}^{M-1} {\sum_{j=0}^{N-1}{(n_x - \overline{n_x}) * f(n_x, n_y)}} / L_1_norm
x, y = np.meshgrid(np.arange(0, 256), np.arange(0, 256))
x_0 = np.sum(x * image) / L_1_norm # image is binary, so \sum_{i,j} x[i, j] = \sum_{i,j} abs(x[i, j]) = L_1_norm
print("x_0: ", x_0)
y_0 = np.sum(y * image) / L_1_norm
print("y_0: ", y_0)
m_2_0 = np.sum(((x - x_0)**2) * image) / L_1_norm
m_0_2 = np.sum(((y - y_0)**2) * image) / L_1_norm
m_1_1 = np.sum(((x - x_0) * (y - y_0)) * image) / L_1_norm
print("m_2_0: ", m_2_0)
print("m_0_2: ", m_0_2)
print("m_1_1: ", m_1_1)
# L0 norm:  6417
# L1 norm:  6417
# L2 norm:  80.10617953691214
# L_infinity norm:  1
# x_0:  64.0
# y_0:  128.0
# m_2_0:  1023.6047997506623
# m_0_2:  254.75455820476859
# m_1_1:  0.0