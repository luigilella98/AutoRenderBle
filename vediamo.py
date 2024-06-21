import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import matplotlib.pyplot as plt
import cv2

img = cv2.imread("./renders/VESKEN/DEPTH/posa_000_depth.exr", cv2.IMREAD_UNCHANGED)

plt.imshow(img[:,:,0])
plt.show()