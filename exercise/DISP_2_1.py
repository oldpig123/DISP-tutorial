import cv2
import numpy as np

# variance
def variance(img):
    mu = np.mean(img)
    var = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                var += (img[i,j,k] - mu) ** 2
    var = var / (img.shape[0] * img.shape[1]*img.shape[2])
    return var

# covariance
def covariance(img1, img2):
    mu_x = np.mean(img1)
    mu_y = np.mean(img2)
    cov = 0
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            for k in range(img1.shape[2]):
                cov += (img1[i,j,k] - mu_x) * (img2[i,j,k] - mu_y)
    cov = cov / (img1.shape[0] * img1.shape[1]*img1.shape[2])
    return cov

# SSIM
def SSIM(img1, img2):
    # L is the maximal possible pixel value - minimal possible pixel value
    L = 255
    # c_1 and c_2 are both adjustable constants
    c_1 = np.sqrt(1/L)
    c_2 = np.sqrt(1/L) # that is what tutorial says
    # mu_x and mu_y are the mean of the images
    mu_x = np.mean(img1)
    mu_y = np.mean(img2)
    # sigma_x_square and sigma_y_square are the variance of the images
    sigma_x_square = variance(img1) # or just np.var(img1)
    sigma_y_square = variance(img2) # or just np.var(img2)
    # sigma_xy is the covariance of the images
    sigma_xy = covariance(img1, img2)

    ssim = (2 * mu_x * mu_y + (c_1*L)**2) * (2 * sigma_xy + (c_2*L)**2) / ((mu_x ** 2 + mu_y ** 2 + (c_1*L)**2) * (sigma_x_square + sigma_y_square + (c_2*L)**2))
    return ssim

img_original = cv2.imread("Pic/peppers.bmp")
if img_original is None:
    raise FileNotFoundError("Could not find Pic/peppers.bmp")
img_laplacian = cv2.imread("exercise/DISP_1/result_laplacian_manual_convolution.png")
if img_laplacian is None:
    raise FileNotFoundError("Could not find exercise/DISP_1/result_laplacian_manual_convolution.png. Please run DISP_1_1.py first.")
img_lighten_cv = cv2.imread("exercise/DISP_1/lighten_cv.png")
if img_lighten_cv is None:
    raise FileNotFoundError("Could not find exercise/DISP_1/lighten_cv.png. Please run DISP_1_2.py first.")
img_darken_cv = cv2.imread("exercise/DISP_1/darken_cv.png")
if img_darken_cv is None:
    raise FileNotFoundError("Could not find exercise/DISP_1/darken_cv.png. Please run DISP_1_2.py first.")

print("SSIM (Original vs Laplacian):", SSIM(img_original, img_laplacian))
print("SSIM (Original vs Lighten):  ", SSIM(img_original, img_lighten_cv))
print("SSIM (Original vs Darken):   ", SSIM(img_original, img_darken_cv))
print("SSIM (Lighten vs Darken):    ", SSIM(img_lighten_cv, img_darken_cv))

# SSIM (Original vs Laplacian): 0.004394418540015819
# SSIM (Original vs Lighten):   0.9211026722997963
# SSIM (Original vs Darken):    0.8281487684121199
# SSIM (Lighten vs Darken):     0.6475509420839456