import cv2
import numpy as np

# NRMSE
def NRMSE(img1, img2):
    sqaure_error = 0.0
    energy = 0.0
    
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            for k in range(img1.shape[2]):
                sqaure_error += (float(img1[i,j,k]) - float(img2[i,j,k])) ** 2
                energy += float(img1[i,j,k]) ** 2
    
    nrmse = np.sqrt(sqaure_error) / np.sqrt(energy)
    return nrmse

# PSNR
def PSNR(img1, img2):
    sqaure_error = 0.0
    X_Max = 255.0
    
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            for k in range(img1.shape[2]):
                sqaure_error += (float(img1[i,j,k]) - float(img2[i,j,k])) ** 2
    
    mse = sqaure_error / (img1.shape[0] * img1.shape[1] * img1.shape[2])
    psnr = 10 * np.log10(X_Max**2 / mse)
    return psnr

img_original = cv2.imread("Pic/peppers.bmp")
img_laplacian = cv2.imread("exercise/DISP_1/result_laplacian_manual_convolution.png")
img_lighten_cv = cv2.imread("exercise/DISP_1/lighten_cv.png")
img_darken_cv = cv2.imread("exercise/DISP_1/darken_cv.png")

print("NRMSE of Laplacian:", NRMSE(img_original, img_laplacian))
print("PSNR of Laplacian:", PSNR(img_original, img_laplacian))
print("NRMSE of lighten_cv:", NRMSE(img_original, img_lighten_cv))
print("PSNR of lighten_cv:", PSNR(img_original, img_lighten_cv))
print("NRMSE of darken_cv:", NRMSE(img_original, img_darken_cv))
print("PSNR of darken_cv:", PSNR(img_original, img_darken_cv))
print("NRMSE between lighten_cv and darken_cv:", NRMSE(img_lighten_cv, img_darken_cv))
print("PSNR between lighten_cv and darken_cv:", PSNR(img_lighten_cv, img_darken_cv))

# NRMSE of Laplacian: 0.8708793084529113
# PSNR of Laplacian: 7.125071912666955
# NRMSE of lighten_cv: 0.3851737502144378
# PSNR of lighten_cv: 14.21109771339072
# NRMSE of darken_cv: 0.395420139081962
# PSNR of darken_cv: 13.983055664324983
# NRMSE between lighten_cv and darken_cv: 0.5784730974074892
# PSNR between lighten_cv and darken_cv: 8.291846334357892
