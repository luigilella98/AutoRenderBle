import cv2

# Load the image
image_path = "../renders/gt_01_gt/0000000000.png"
image = cv2.imread(image_path)
img = image[:,:,1]
print(img.shape)
print(img.max())
