import cv2
import numpy as np

# brightness adjustment
def brightness_adjustment_cv2(img, alpha): # alpha is the brightness adjustment factor
    # image load by cv2.imread is BGR
    # convert to YCbCr
    img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_ycrcb)
    y = 255*(y/255)**alpha
    y = np.clip(y, 0, 255)
    y = y.astype(np.uint8)
    img_ycrcb = cv2.merge((y, cr, cb))
    img_bgr = cv2.cvtColor(img_ycrcb, cv2.COLOR_YCrCb2BGR)
    return img_bgr

def brightness_adjustment_manual(img, alpha):
    b, g, r = cv2.split(img)
    # stack r, g, b
    rgb = np.dstack((r, g, b))
    # convert to ycbcr
    # convert with matrix
    convert_matrix = np.array([[0.299, 0.587, 0.114], [-0.168736, -0.331264, 0.5], [0.5, -0.418688, -0.081312]])
    # matrix multiply
    ycbcr = np.dot(rgb, convert_matrix.T)
    # apply alpha
    ycbcr[:,:,0] = 255*(ycbcr[:,:,0]/255)**alpha    
    ycbcr[:,:,0] = np.clip(ycbcr[:,:,0], 0, 255)
    # ycbcr = ycbcr.astype(np.uint8)
    new_rgb = np.dot(ycbcr, np.linalg.inv(convert_matrix).T)
    final_bgr = new_rgb[:,:,[2,1,0]]
    final_bgr = np.clip(final_bgr, 0, 255)
    final_bgr = final_bgr.astype(np.uint8)

    return final_bgr
    

img = cv2.imread("Pic/peppers.bmp")
lighten_factor = 0.5
darken_factor = 1.5
lighten_cv = brightness_adjustment_cv2(img, lighten_factor)
darken_cv = brightness_adjustment_cv2(img, darken_factor)
lighten_manual = brightness_adjustment_manual(img, lighten_factor)
darken_manual = brightness_adjustment_manual(img, darken_factor)

cv2.imwrite("exercise/DISP_1/lighten_cv.bmp", lighten_cv)
cv2.imwrite("exercise/DISP_1/darken_cv.bmp", darken_cv)
cv2.imwrite("exercise/DISP_1/lighten_manual.bmp", lighten_manual)
cv2.imwrite("exercise/DISP_1/darken_manual.bmp", darken_manual)


