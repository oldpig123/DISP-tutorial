import cv2
import numpy as np
image = cv2.imread("Pic/peppers.bmp")
if image is None:
    raise FileNotFoundError("Could not find Pic/peppers.bmp")
print(image.shape) # (height, width, channel) = (512, 512, 3)

# cv2.imshow("image", image)
# cv2.waitKey(0)
cv2.destroyAllWindows()

# import matplotlib.pyplot as plt
# plt.imshow(image[:,:,[2,1,0]])
# # plt.show()
# matplotlib # plt.show() remain skip due to graphic driver error as below
# QFontDatabase: Cannot find font directory /media/nmlab326/b2cd0f5f-2bd7-46c8-8a50-58708471c1bf1/DISP_data/.venv/lib/python3.12/site-packages/cv2/qt/fonts.
# Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.
# QFontDatabase: Cannot find font directory /media/nmlab326/b2cd0f5f-2bd7-46c8-8a50-58708471c1bf1/DISP_data/.venv/lib/python3.12/site-packages/cv2/qt/fonts.
# Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.
# QFontDatabase: Cannot find font directory /media/nmlab326/b2cd0f5f-2bd7-46c8-8a50-58708471c1bf1/DISP_data/.venv/lib/python3.12/site-packages/cv2/qt/fonts.
# Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.
# QFontDatabase: Cannot find font directory /media/nmlab326/b2cd0f5f-2bd7-46c8-8a50-58708471c1bf1/DISP_data/.venv/lib/python3.12/site-packages/cv2/qt/fonts.
# Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.
# QFontDatabase: Cannot find font directory /media/nmlab326/b2cd0f5f-2bd7-46c8-8a50-58708471c1bf1/DISP_data/.venv/lib/python3.12/site-packages/cv2/qt/fonts.
# Note that Qt no longer ships fonts. Deploy some (from https://dejavu-fonts.github.io/ for example) or switch to fontconfig.
# QObject::moveToThread: Current thread (0x3e13a110) is not the object's thread (0x3d656250).
# Cannot move to target thread (0x3e13a110)

# qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/media/nmlab326/b2cd0f5f-2bd7-46c8-8a50-58708471c1bf1/DISP_data/.venv/lib/python3.12/site-packages/cv2/qt/plugins" even though it was found.
# This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

# Available platform plugins are: xcb, eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl.

image1 = image * 0.5 + 127.5
# cv2.imshow("test", image1)
# cv2.waitKey(0)
cv2.destroyAllWindows()

# cv2.imshow("test", image1/255)
# cv2.waitKey(0)
cv2.destroyAllWindows()

# save image1 as the result before /255 and save image1/255 as the result after /255
# save at exercise/multi_media_r_w_2/
cv2.imwrite("exercise/multi_media_r_w_2/image1_before_div_255.png", image1.astype(np.uint8))
cv2.imwrite("exercise/multi_media_r_w_2/image1_after_div_255.png", (image1/255).astype(np.uint8))
