import numpy as np
import cv2
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view

# erosion (vectorized)
def erosion_vectorized(img, kernel):
    # get the size of image and kernel
    img_h, img_w = img.shape
    kernel_h, kernel_w = kernel.shape
    # create the output image
    output = np.zeros_like(img)
    # padding the image
    pad_h = kernel_h // 2
    pad_w = kernel_w // 2
    padded_img = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    # get the sliding window view
    sliding_window = sliding_window_view(padded_img, (kernel_h, kernel_w))
    # get the minimum value of the product
    output = np.min(sliding_window[:,:,kernel == 1], axis=2)
    return output

# dilation (vectorized)
def dilation_vectorized(img, kernel):
    # get the size of image and kernel
    img_h, img_w = img.shape
    kernel_h, kernel_w = kernel.shape
    # create the output image
    output = np.zeros_like(img)
    # padding the image
    pad_h = kernel_h // 2
    pad_w = kernel_w // 2
    padded_img = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    # get the sliding window view
    sliding_window = sliding_window_view(padded_img, (kernel_h, kernel_w))
    # get the maximum value of the product
    output = np.max(sliding_window[:,:,kernel == 1], axis=2)
    return output

# opening (vectorized)
def opening_vectorized(img, kernel,k):
    output = img
    for _ in range(k):
        output = erosion_vectorized(output, kernel)
    for _ in range(k):
        output = dilation_vectorized(output, kernel)
    return output

# closing (vectorized)
def closing_vectorized(img, kernel,k):
    output = img
    for _ in range(k):
        output = dilation_vectorized(output, kernel)
    for _ in range(k):
        output = erosion_vectorized(output, kernel)
    return output

# erosion
def erosion(img, kernel):
    # get the size of image and kernel
    img_h, img_w = img.shape
    kernel_h, kernel_w = kernel.shape
    # create the output image
    output = np.zeros_like(img)
    # padding the image
    pad_h = kernel_h // 2
    pad_w = kernel_w // 2
    padded_img = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    # iterate over the image
    for i in range(img_h):
        for j in range(img_w):
            # get the neighborhood of the current pixel
            neighborhood = padded_img[i:i+kernel_h, j:j+kernel_w]
            # get the minimum value of the product
            output[i, j] = np.min(neighborhood[kernel == 1])
    return output

# dilation
def dilation(img, kernel):
    # get the size of image and kernel
    img_h, img_w = img.shape
    kernel_h, kernel_w = kernel.shape
    # create the output image
    output = np.zeros_like(img)
    # padding the image
    pad_h = kernel_h // 2
    pad_w = kernel_w // 2
    padded_img = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    # iterate over the image
    for i in range(img_h):
        for j in range(img_w):
            # get the neighborhood of the current pixel
            neighborhood = padded_img[i:i+kernel_h, j:j+kernel_w]
            # get the maximum value of the product
            output[i, j] = np.max(neighborhood[kernel == 1])
    return output

# opening
# opening is erosion k times followed by dilation k times
def opening(img, kernel,k):
    output = img
    for _ in range(k):
        output = erosion(output, kernel)
    for _ in range(k):
        output = dilation(output, kernel)
    return output

# closing
# closing is dilation k times followed by erosion k times
def closing(img, kernel,k):
    output = img
    for _ in range(k):
        output = dilation(output, kernel)
    for _ in range(k):
        output = erosion(output, kernel)
    return output
            
# load lena image
img = cv2.imread("Pic/gray512/Lena.png", cv2.IMREAD_GRAYSCALE)
# create a kernel
kernel = np.ones((3,3), dtype=np.uint8)
# define how many times to apply the operation
k = 3

# apply erosion k times
erosion_img = img
for _ in range(k):
    erosion_img = erosion_vectorized(erosion_img, kernel)

# apply dilation k times
dilation_img = img
for _ in range(k):
    dilation_img = dilation_vectorized(dilation_img, kernel)

# apply openning with each element operation k times
opening_img = opening_vectorized(img, kernel, k)
# apply closing with each element operation k times
closing_img = closing_vectorized(img, kernel, k)

# save images in one figure
# arrange like this
# origin | erosion | dilation
#        | opening | closing
# total 3 rows, 2 columns
plt.figure(figsize=(12, 6))
plt.subplot(2, 3, 1)
plt.imshow(img, cmap='gray')
plt.title("origin")
plt.subplot(2, 3, 2)
plt.imshow(erosion_img, cmap='gray')
plt.title("erosion")
plt.subplot(2, 3, 3)
plt.imshow(dilation_img, cmap='gray')
plt.title("dilation")
plt.subplot(2, 3, 5)
plt.imshow(opening_img, cmap='gray')
plt.title("opening")
plt.subplot(2, 3, 6)
plt.imshow(closing_img, cmap='gray')
plt.title("closing")
plt.tight_layout()
plt.savefig("exercise/DISP_3/morphological_operations.png")
plt.clf()