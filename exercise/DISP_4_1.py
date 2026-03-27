import numpy as np 
import cv2
import matplotlib.pyplot as plt

# kernel generator
# a gaussian-like blur kernel
def kernel_generator(kernel_size_bound):
    m, n = np.meshgrid(np.arange(-kernel_size_bound, kernel_size_bound + 1), np.arange(-kernel_size_bound, kernel_size_bound + 1)) 

    # kernel[m, n] = s * exp[-0.1 * (m^2 + n^2)]
    # s = 1/sum(sum(exp[-0.1 * (m^2 + n^2)], n from -kernel_size_bound to kernel_size_bound), m from -kernel_size_bound to kernel_size_bound)
    s = 1/np.sum(np.exp(-0.1 * (m**2 + n**2)))
    kernel = s * np.exp(-0.1 * (m**2 + n**2))
    return kernel

# noise generator
def noise_generator(img, noise_level):
    # generate with rand function
    noise = np.random.rand(img.shape[0], img.shape[1])-0.5
    noise = noise * noise_level
    return img + noise

# restoration function
def restoration(img, kernel, C):
    # extent and pad the kernel to the same size as the image
    kernel_size_bound = kernel.shape[0]//2
    M = img.shape[0] - kernel_size_bound
    N = img.shape[1] - kernel_size_bound
    kernel_extended = np.zeros((img.shape[0], img.shape[1]))
    
    # kernel_1 [m,n] = kernel[m,n] if 0 <= m,n <= kernel_size_bound
    # top-left
    kernel_extended[0:kernel_size_bound+1, 0:kernel_size_bound+1] = kernel[kernel_size_bound:, kernel_size_bound:]
    # kernel_1 [m + M,n] = kernel[m,n] if -kernel_size_bound <= m < 0 and 0 <= n <= kernel_size_bound
    # bottom-left
    kernel_extended[M:, 0:kernel_size_bound+1] = kernel[0:kernel_size_bound, kernel_size_bound:]
    # kernel_1 [m,n + N] = kernel[m,n] if 0 <= m <= kernel_size_bound and -kernel_size_bound <= n < 0
    # top-right
    kernel_extended[0:kernel_size_bound+1, N:] = kernel[kernel_size_bound:, 0:kernel_size_bound]
    # kernel_1 [m + M,n + N] = kernel[m,n] if -kernel_size_bound <= m < 0 and -kernel_size_bound <= n < 0
    # bottom-right
    kernel_extended[M:, N:] = kernel[0:kernel_size_bound, 0:kernel_size_bound]

    # fft both img and kernel
    img_fft = np.fft.fft2(img)
    kernel_extended_fft = np.fft.fft2(kernel_extended)
    
    # define EQ with kernel_extended_fft and C
    # EQ = 1/(kernel_extended_fft + C/conjugaet of kernel_extended_fft)
    eq = equalizer_defination(kernel_extended_fft, C)
    
    # restore image
    img_restored_fft = img_fft * eq
    img_restored = np.clip(np.abs(np.fft.ifft2(img_restored_fft)), 0, 255)
    return img_restored
    

# define EQ with kernel_extended_fft and C
# EQ = 1/(kernel_extended_fft + C/conjugaet of kernel_extended_fft)
def equalizer_defination(kernel_extended_fft, C):
    return 1/(kernel_extended_fft + C/np.conj(kernel_extended_fft))


img = cv2.imread("Pic/gray512/Lena.png", cv2.IMREAD_GRAYSCALE).astype(np.float32)
kernel = kernel_generator(10)
# blur with kernel
img_blur = cv2.filter2D(img, -1, kernel)
# set noise level list with two different values
noise_level = [10, 50]
# C should base on SNR, but here we just set it as adjustable constant from 0.01 to 0.2  with 2 different values
C = [0.01, 0.05]
# test with two different noise levels and two different C values
# show the original image, blurred image, noisy image, and restored image
# arrange like this
# original | blurred
# noisy_1 | restored_1 |restored_2
# noisy_2 | restored_3 |restored_4
# total 3 rows, 3 columns

# show original image and blurred image
plt.figure(figsize=(12, 12))
plt.subplot(3, 3, 1)
plt.imshow(img, cmap='gray')
plt.title("original")
plt.subplot(3, 3, 2)
plt.imshow(img_blur, cmap='gray')
plt.title("blurred")

# show noisy image and restored image
for i in range(2):
    # add noise
    img_noisy = noise_generator(img_blur, noise_level[i])
    # restore image
    # mg_restored = restoration(img_noisy, kernel, C[i])
    # show noisy image
    plt.subplot(3, 3, i*3 + 3+1)
    plt.imshow(img_noisy, cmap='gray')
    plt.title("noise level: " + str(noise_level[i]))
    # show restored image with C[i]
    for j in range(2):
        img_restored = restoration(img_noisy, kernel, C[j])
        plt.subplot(3, 3, i*3 + 3+1 + j + 1)
        plt.imshow(img_restored, cmap='gray', vmin=0, vmax=255)
        plt.title("restore with C = " + str(C[j]))

plt.tight_layout()

plt.savefig("exercise/DISP_4/original_and_blurred_and_restored.png")
plt.clf()

