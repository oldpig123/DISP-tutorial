import cv2
import numpy as np

# sobel operator function
def sobel_operator(img, operator):
    result = cv2.filter2D(img, cv2.CV_64F, operator)/4.0
    result = np.abs(result*5)
    result = np.clip(result, 0, 255)
    result = result.astype(np.uint8)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    return result

# laplacian operator function
def laplacian_operator(img, operator):
    result = cv2.filter2D(img, cv2.CV_64F, operator)/8.0
    result = np.abs(result*5)
    result = np.clip(result, 0, 255)
    result = result.astype(np.uint8)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    return result

img = cv2.imread("Pic/peppers.bmp")
laplacian = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

# 1. Using manually construct 2D convolution
    
height, width, channel = img.shape
kernel_height, kernel_width = laplacian.shape
result = np.zeros((height, width, channel), dtype=np.float32)
for i in range(1, height -1):
    for j in range(1, width -1):
        for k in range(channel):
            result[i, j, k] = np.sum(img[i-1:i+2, j-1:j+2, k] * laplacian)/8.0

# apply "C * abs(E)" Rule
result = np.abs(result*5)
# clip image result
result = np.clip(result, 0, 255)
result = result.astype(np.uint8)
#make it graylevel
result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
#save result as result_laplacian_manual_convolution.bmp
cv2.imwrite("exercise/DISP_1/result_laplacian_manual_convolution.bmp", result)


# 2. Using cv2.filter2D
result = laplacian_operator(img, laplacian)
# save result as result_laplacian_cv_convolution.bmp
cv2.imwrite("exercise/DISP_1/result_laplacian_cv_convolution.bmp", result)

# horizontal sobel operator
sobel_horizontal = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
result = sobel_operator(img, sobel_horizontal)
cv2.imwrite("exercise/DISP_1/result_horizontal_sobel.bmp", result)

# vertical sobel operator
sobel_vertical = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
result = sobel_operator(img, sobel_vertical)
cv2.imwrite("exercise/DISP_1/result_vertical_sobel.bmp", result)

# 135 degree sobel operator
sobel_135 = np.array([[0,-1,-2],[1,0,-1],[2,1,0]])
result = sobel_operator(img, sobel_135)
cv2.imwrite("exercise/DISP_1/result_135_sobel.bmp", result)

# 45 degree sobel operator
sobel_45 = np.array([[-2,-1,0],[-1,0,1],[0,1,2]])
result = sobel_operator(img, sobel_45)
cv2.imwrite("exercise/DISP_1/result_45_sobel.bmp", result)
