import cv2
import os

FOLDER_PATH = './renders/'

def create_binary_images(folder_path):

    for root, dirs, _ in os.walk(folder_path):
        for dir_name in dirs:
            
            if dir_name.endswith('_gt'):
                gt_folder_path = os.path.join(root, dir_name)
                print(f"Processing folder: {gt_folder_path}")
               
                for filename in os.listdir(gt_folder_path):
                    
                    img_path = os.path.join(gt_folder_path, filename)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    _, binary_img = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)
                    cv2.imwrite(img_path, binary_img)
                    print(f"Binary image saved: {img_path}")


create_binary_images(FOLDER_PATH)