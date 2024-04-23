import cv2
import matplotlib.pyplot as plt
# Load the image
image_path = "../renders/fat_cat_gt/posa_000.png"
image = cv2.imread(image_path)
img = image[:,:,1]
plt.imshow(image)
plt.show()