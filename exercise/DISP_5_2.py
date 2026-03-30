import numpy as np
import cv2
import matplotlib.pyplot as plt

# resize and perform bilinear interpolation
# input image size is M by N, output image size is M' by N', which is (M*k, N*l)
# k and l are the scaling factors
def resize_bilinear(image, k, l):
    # handle rgb image
    if len(image.shape) == 3:
        M, N, C = image.shape
    else: 
        M, N = image.shape
        C = 1
    n_prime, m_prime = np.meshgrid(np.arange(int(N*l)), np.arange(int(M*k)))
    m_prime_ori = m_prime/k
    n_prime_ori = n_prime/l
    #vectorized bilinear interpolation
    m_prime_floor = np.floor(m_prime_ori).astype(int)
    n_prime_floor = np.floor(n_prime_ori).astype(int)
    m_prime_next = m_prime_floor + 1
    n_prime_next = n_prime_floor + 1
    # a for vertical interpolation, b for horizontal interpolation
    a = m_prime_ori - m_prime_floor
    b = n_prime_ori - n_prime_floor
    if C == 3:
        a = a[:, :, np.newaxis]
        b = b[:, :, np.newaxis]
    # boundary check
    m_prime_next = np.clip(m_prime_next, 0, M-1)
    n_prime_next = np.clip(n_prime_next, 0, N-1)
    m_prime_floor = np.clip(m_prime_floor, 0, M-1)
    n_prime_floor = np.clip(n_prime_floor, 0, N-1)
    # bilinear interpolation
    image_output = (1-a)*(1-b)*image[m_prime_floor, n_prime_floor] + (1-a)*b*image[m_prime_floor, n_prime_next] + a*(1-b)*image[m_prime_next, n_prime_floor] + a*b*image[m_prime_next, n_prime_next]
    return image_output

# load and test with pepper image
image = cv2.imread("Pic/peppers.bmp")
if image is None:
    raise FileNotFoundError("Could not find Pic/peppers.bmp")
image_output = resize_bilinear(image, 1.5, 1.6)

# Convert the float64 interpolation result back to uint8!
image_output = np.clip(image_output, 0, 255).astype(np.uint8)

# creat canvas to show original and output image
h_max = max(image.shape[0], image_output.shape[0])
w_total = image.shape[1] + image_output.shape[1] + 50
canvas = np.zeros((h_max, w_total, 3), dtype=np.uint8)
canvas[0:image.shape[0], 0:image.shape[1], :] = image
canvas[0:image_output.shape[0], image.shape[1]+50:, :] = image_output

# save original and output image in one image
cv2.imwrite("exercise/DISP_5/original_and_output_image.png", canvas)