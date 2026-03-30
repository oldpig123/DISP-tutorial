import numpy as np
import cv2
import matplotlib.pyplot as plt

# picture merge 
# merge high frequency of one picture and low frequency of another picture
# L is the cut off frequency
def picture_merge(img1, img2, window_size):
    # check the size of two image match
    if img1.shape != img2.shape:
        raise ValueError("The size of two image must match")

    # L = N/window size
    N = img1.shape[0]
    L = N/window_size

    # fft of two image 
    img1_fft = np.fft.fft2(img1, axes=(0,1))
    img2_fft = np.fft.fft2(img2, axes=(0,1))
    # do fft shift
    img1_fft = np.fft.fftshift(img1_fft, axes=(0,1))
    img2_fft = np.fft.fftshift(img2_fft, axes=(0,1))

    # difine row, column and center index
    row, col = img1.shape[0], img1.shape[1]
    center_row, center_col = row//2, col//2

    # create mask
    y,x = np.ogrid[:row, :col]

    # distance from center
    # dist_from_center = np.sqrt((x - center_col)**2 + (y - center_row)**2)
    dist_from_center = np.abs(x - center_col) + np.abs(y - center_row)

    # creat mask
    mask = (dist_from_center <= L)[:,:,np.newaxis]

    # low pass for img1
    img1_low = np.where(mask, img1_fft, 0)

    # high pass for img2
    img2_high = np.where(~mask, img2_fft, 0)

    # merge two image
    img_merge = img1_low + img2_high
    
    # make img_merge can be displayed
    img_final = np.abs(np.fft.ifft2(np.fft.ifftshift(img_merge, axes=(0,1)), axes=(0,1)))
    
    return img_final, np.abs(np.fft.ifft2(np.fft.ifftshift(img1_low, axes=(0,1)), axes=(0,1))), np.abs(np.fft.ifft2(np.fft.ifftshift(img2_high, axes=(0,1)), axes=(0,1)))



# image
lena = cv2.imread("Pic/gray512/Lena.png")
if lena is None:
    raise FileNotFoundError("Could not find Pic/gray512/Lena.png")
barbara = cv2.imread("Pic/gray512/Barbara.png")
if barbara is None:
    raise FileNotFoundError("Could not find Pic/gray512/Barbara.png")

merge_img, img1_low, img2_high = picture_merge(lena, barbara, 30)

# save images in one figure
# arrange like this
# img1 | low pass img1
# img2 | high pass img2
# merge img
# total 3 rows, 2 columns
# change every image to RGB for matplotlib 
lena = cv2.cvtColor(lena, cv2.COLOR_BGR2RGB)
barbara = cv2.cvtColor(barbara, cv2.COLOR_BGR2RGB)
# for funtion returned image, we should normalize it first and make it uint8
img1_low = cv2.normalize(img1_low, img1_low, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
img2_high = cv2.normalize(img2_high, img2_high, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
merge_img = cv2.normalize(merge_img, merge_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
img1_low = img1_low.astype(np.uint8)
img2_high = img2_high.astype(np.uint8)
merge_img = merge_img.astype(np.uint8)
img1_low = cv2.cvtColor(img1_low, cv2.COLOR_BGR2RGB)
img2_high = cv2.cvtColor(img2_high, cv2.COLOR_BGR2RGB)
merge_img = cv2.cvtColor(merge_img, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(12, 6))
plt.subplot(3, 3, 1)
plt.imshow(lena)
plt.title("lena")
plt.subplot(3, 3, 2)
plt.imshow(img1_low)
plt.title("low pass lena")
plt.subplot(3,3,3)
plt.imshow(np.log(1+np.abs(np.fft.ifftshift(np.fft.fft2(lena, axes=(0,1)), axes=(0,1)))).mean(axis=2), cmap='gray')
plt.title("fft lena")
plt.subplot(3, 3, 4)
plt.imshow(barbara)
plt.title("barbara")
plt.subplot(3, 3, 5)
plt.imshow(img2_high)
plt.title("high pass barbara")
plt.subplot(3,3,6)
plt.imshow(np.log(1+np.abs(np.fft.ifftshift(np.fft.fft2(barbara, axes=(0,1)), axes=(0,1)))).mean(axis=2), cmap='gray')
plt.title("fft barbara")
plt.subplot(3, 3, 7)
plt.imshow(merge_img)
plt.title("merge img")
plt.subplot(3,3,9)
plt.imshow(np.log(1+np.abs(np.fft.ifftshift(np.fft.fft2(merge_img, axes=(0,1)), axes=(0,1)))).mean(axis=2), cmap='gray')
plt.title("fft merge img")
#tight layout
plt.tight_layout()
plt.savefig("exercise/DISP_3/merge_img.png")
plt.clf()