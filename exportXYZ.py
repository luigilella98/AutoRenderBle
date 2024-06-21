import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import cv2
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from tqdm import tqdm  # Import tqdm

NAME = "VESKMEZZO"
DEPTH_PATH = "./renders/" + NAME + "/DEPTH"
OUTPUT_PATH = "./renders/" + NAME + "/XYZ"  

def load_depth(dpath):
    depths = []
    if os.path.isdir(dpath):
        for f in tqdm(os.listdir(dpath)):
            if f.endswith(".exr"):
                depths.append(cv2.imread(os.path.join(dpath, f), cv2.IMREAD_UNCHANGED))
    return depths

depths = load_depth(DEPTH_PATH)

focal_length = 3.4702761957637335e+03
cx = 2.0457960174875925e+03
cy = 1.5636291650560495e+03 

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

for idx, depth in tqdm(enumerate(depths), total=len(depths)):
    h, w = depth.shape[:2]
    mesh_x, mesh_y = np.meshgrid(range(w), range(h))
    mesh_points = np.dstack((mesh_x, mesh_y)).reshape(-1, 2)
    depth_values = depth[:,:,0].reshape(-1)
    
    pcd = np.zeros((mesh_points.shape[0],3))
    pcd[:,0] = (mesh_points[:,0] - cx) * depth_values / focal_length
    pcd[:,1] = (mesh_points[:,1] - cy) * depth_values / focal_length
    pcd[:,2] = depth_values
    
    xyz = pcd.reshape([h,w,3])
    xyz[depth[:,:,0] > 100] = [0, 0, 0]

    xyz = xyz.astype(np.float32)
    
    cv2.imwrite(os.path.join(OUTPUT_PATH, "posa_{:03d}_XYZ.exr".format(idx)), xyz)
    
