import cv2
image = cv2.imread("Pic/peppers.bmp")
print(image.shape) # (height, width, channel) = (512, 512, 3)

cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import matplotlib.pyplot as plt
plt.imshow(image[:,:,[2,1,0]])
plt.show()