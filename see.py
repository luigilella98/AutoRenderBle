'''import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('untitled.png')
plt.imshow(img)
plt.show()'''
import numpy as np
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

import cv2

try:
    new = cv2.imread('C:/Users/luigi/Desktop/depth.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)  
    if new is None:
        raise FileNotFoundError("AAAAAAAAAAAAAAAAAAAAAAAAA")
    

except FileNotFoundError as e:
    print("Errore:", e)

print(new.shape)
print(np.max(new))
print(np.min(new))

def unique_elements(matrix):
    unique_list = []
    for channel in matrix:
        unique_channel = np.unique(channel)
        unique_list.extend(unique_channel.tolist())
    unique_list = list(set(unique_list))  # Rimuove duplicati
    return unique_list

boh = unique_elements(new)

print(len(boh))

cv2.imshow('exr', new)
cv2.waitKey(0)
cv2.destroyAllWindows()
