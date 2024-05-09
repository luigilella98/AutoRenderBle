import matplotlib.pyplot as plt
import cv2
depth_map = cv2.imread('C:/Users/luigi/Desktop/003.tiff', cv2.IMREAD_UNCHANGED)
print(depth_map.min(), depth_map.max())


plt.imshow(depth_map)
plt.show()