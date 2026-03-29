import numpy as np
import cv2
import matplotlib.pyplot as plt

# transform function
def transform(image, transform_matrix):
    # rotation
    inverse_transform_matrix = np.linalg.inv(transform_matrix)
    # center of image
    c_m, c_n = image.shape[0]//2, image.shape[1]//2
    # grid of target image
    n_2, m_2 = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
    # translate to origin
    n_2_shifted = n_2 - c_n
    m_2_shifted = m_2 - c_m
    # flatten to 2 by m*n matrix
    coord_shifted = np.stack([n_2_shifted.flatten(), m_2_shifted.flatten()])
    # rotate to original coordinate
    original_coord = inverse_transform_matrix @ coord_shifted
    # get original coordinate
    n_1 = original_coord[0, :].reshape(image.shape[0], image.shape[1])
    m_1 = original_coord[1, :].reshape(image.shape[0], image.shape[1])
    # translate back to original coordinate
    n_1 = n_1 + c_n
    m_1 = m_1 + c_m
    # apply bilinear interpolation (in exercise 5-2) in each channel without heavy for-loop
    # get a and b for bilinear interpolation
    a = m_1 - np.floor(m_1)
    b = n_1 - np.floor(n_1)
    
    # Enable Color Broadcast via shape expansion
    if len(image.shape) == 3:
        a = a[:, :, np.newaxis]
        b = b[:, :, np.newaxis]

    # get the four nearest neighbors
    n_1_floor = np.floor(n_1).astype(int)
    m_1_floor = np.floor(m_1).astype(int)
    n_1_next = n_1_floor + 1
    m_1_next = m_1_floor + 1
    # apply boundary condition safely (m is row, n is col)
    m_1_floor = np.clip(m_1_floor, 0, image.shape[0]-1)
    n_1_floor = np.clip(n_1_floor, 0, image.shape[1]-1)
    m_1_next = np.clip(m_1_next, 0, image.shape[0]-1)
    n_1_next = np.clip(n_1_next, 0, image.shape[1]-1)
    # apply bilinear interpolation in each channel
    image_output = (1-a)*(1-b)*image[m_1_floor, n_1_floor] + (1-a)*b*image[m_1_floor, n_1_next] + a*(1-b)*image[m_1_next, n_1_floor] + a*b*image[m_1_next, n_1_next]
    
    # zero-out the 'smeared' invalid coordinates that got clamped by np.clip!
    valid_mask = (m_1 >= 0) & (m_1 < image.shape[0]) & (n_1 >= 0) & (n_1 < image.shape[1])
    if len(image.shape) == 3:
        valid_mask = valid_mask[:, :, np.newaxis]
    image_output = image_output * valid_mask
    
    # Prevent the OpenCV Float depth tracker error!
    return np.clip(image_output, 0, 255).astype(np.uint8)

# use peppers.bmp to test
image = cv2.imread("Pic/peppers.bmp")
image_output_rotation = transform(image, np.array([[np.cos(30*np.pi/180), -np.sin(30*np.pi/180)], [np.sin(30*np.pi/180), np.cos(30*np.pi/180)]]))
image_output_shearing = transform(image, np.array([[1, 0], [0.3, 1]]))
# convert them as rgb
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_output_rotation = cv2.cvtColor(image_output_rotation, cv2.COLOR_BGR2RGB)
image_output_shearing = cv2.cvtColor(image_output_shearing, cv2.COLOR_BGR2RGB)

# save the original, rotated, and shearing images
# arrange like this
# original | rotated | shearing
# total 1 row, 3 columns
plt.figure(figsize=(18, 6))
plt.subplot(1, 3, 1)
plt.imshow(image)
plt.title("original")
plt.subplot(1, 3, 2)
plt.imshow(image_output_rotation)
plt.title("rotated")
plt.subplot(1, 3, 3)
plt.imshow(image_output_shearing)
plt.title("shearing")
plt.savefig("exercise/DISP_5/peppers_rotated_and_sheared.png")
plt.clf()
