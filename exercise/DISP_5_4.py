import numpy as np
import cv2
import matplotlib.pyplot as plt

# harris corner detector
def harris_corner_detector(image, k, threshold, window_size = 5):
    # convert image to grayscale if not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    gray = np.float32(gray)

    # compute the partial derivatives of the image
    # kernel for X and Y
    kernel_x = np.array([[-1, 0, 1]], dtype = np.float32)
    kernel_y = np.array([[-1], [0], [1]], dtype = np.float32)
    X = cv2.filter2D(gray, cv2.CV_32F, kernel_x)
    Y = cv2.filter2D(gray, cv2.CV_32F, kernel_y)
    
    # gernerate a circular gaussian-like window w
    # w[i, j] = exp(-(i^2 + j^2) / (2 * sigma^2))
    # sigma = 1
    w = np.zeros((window_size, window_size), dtype = np.float32)
    for i in range(window_size):
        for j in range(window_size):
            w[i, j] = np.exp(-((i-window_size//2)**2 + (j-window_size//2)**2) / (2 * 1**2))
    
    # compute the products of the partial derivatives
    X2 = X**2
    Y2 = Y**2
    XY = X * Y
    
    # compute the weighted sums of the products of the partial derivatives
    A = cv2.filter2D(X2, cv2.CV_32F, w)
    B = cv2.filter2D(Y2, cv2.CV_32F, w)
    C = cv2.filter2D(XY, cv2.CV_32F, w)
    
    # compute the Harris corner response function
    det = A * B - C**2
    trace = A + B
    R = det - k * trace**2
    
    # Normalize R to a range of [-1, 1] based on the absolute maximum
    # This ensures our threshold is a clean percentage (like 0.01 = 1%)
    R = R / np.max(np.abs(R))
    
    # Step 4: Classification (Corners, Edges, Flat)
    # A pixel is a Local Maximum if it equals the max value in its 3x3 neighborhood (Dilate)
    local_max = cv2.dilate(R, np.ones((3, 3), np.uint8))
    
    # A pixel is a Local Minimum if it equals the min value in its 3x3 neighborhood (Erode)
    local_min = cv2.erode(R, np.ones((3, 3), np.uint8))
    
    # Create an output classification map (0 = Flat, 1 = Corner, -1 = Edge)
    output = np.zeros_like(R)
    
    # Corner if R > threshold AND R is the local max
    output[(R > threshold) & (R == local_max)] = 1
    
    # Edge if R < -threshold AND R is the local min
    output[(R < -threshold) & (R == local_min)] = -1
    
    return output

# test with pepper image
image = cv2.imread("Pic/peppers.bmp")
# Using threshold=0.01 (1% of the maximum response)
output = harris_corner_detector(image, k = 0.04, threshold = 0.01, window_size = 5)

annotate_image = image.copy()
# find the coordinates of the corners
# annotate_image[output == 1] = [0, 0, 255] <-- this only put a pixel at the corner, hard to see
y_corners, x_corners = np.where(output == 1)
for i in range(len(y_corners)):
    cv2.circle(annotate_image, (x_corners[i], y_corners[i]), radius=3, color=(0, 0, 255), thickness=-1)
# find the coordinates of the edges
# annotate_image[output == -1] = [0, 255, 0] <-- this only put a pixel at the edge, hard to see
y_edges, x_edges = np.where(output == -1)
for i in range(len(y_edges)):
    cv2.circle(annotate_image, (x_edges[i], y_edges[i]), radius=3, color=(0, 255, 0), thickness=-1)
# do nothing for flat regions

# Convert to RGB so matplotlib correctly displays the Bright Red and Bright Green dots!
annotate_image = cv2.cvtColor(annotate_image, cv2.COLOR_BGR2RGB)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# save the annotated image and original image as one single image
plt.figure(figsize=(12, 6), dpi = 300)
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("original")
plt.subplot(1, 2, 2)
plt.imshow(annotate_image)
plt.title("annotated")
plt.savefig("exercise/DISP_5/peppers_harris_corner_detector.png")
plt.clf()

