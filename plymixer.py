import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import cv2
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from tqdm import tqdm

DEPTH_PATH = './prove/depth'
RGB_PATH = './prove/rgb'
POSE_PATH = './prove/pose.txt'

# Caricamento delle depthmaps
def load_depth(dpath):
    depths = []
    if os.path.isdir(dpath):
        for f in tqdm(os.listdir(dpath), desc="Caricamento delle depthmaps"):
            depths.append(cv2.imread(os.path.join(dpath, f), cv2.IMREAD_UNCHANGED))
    return depths

# Caricamento delle RGBs
def load_rgbs(rgbpath):
    rgbs = []
    if os.path.isdir(rgbpath):
        for f in tqdm(os.listdir(rgbpath), desc="Caricamento delle RGBs"):
            img = cv2.imread(os.path.join(rgbpath, f))
            rgbs.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return rgbs


# Caricamento delle pose
def load_poses(posepath):
    pose = open(posepath).readlines()
    poses = []
    for line in tqdm(pose, desc="Caricamento delle pose"):
        splits = line.split(" ")
        mtx = np.zeros([4, 4])
        mtx[3, 3] = 1
        for idx, s in enumerate(splits):
            mtx[idx // 4, idx % 4] = float(s)
        poses.append(mtx)
    return poses

focal_length = 3.4702761957637335e+03  # Focale della tua telecamera
cx = 2.0457960174875925e+03
cy = 1.5636291650560495e+03 

depth = load_depth(DEPTH_PATH)
rgb = load_rgbs(RGB_PATH)
poses = load_poses(POSE_PATH)


ply = []
print("1")
for i in tqdm(range(len(depth)), desc="Elaborazione delle depthmaps"):
    h, w = depth[i].shape[:2]
    mesh_x, mesh_y = np.meshgrid(range(w), range(h))
    mesh_points = np.dstack((mesh_x, mesh_y)).reshape(-1, 2)
    depth_values = depth[i][:, :, 0].reshape(-1)
    point_cloud = np.zeros((mesh_points.shape[0], 3))
    point_cloud[:, 0] = (mesh_points[:, 0] - cx) * depth_values / focal_length
    point_cloud[:, 1] = (mesh_points[:, 1] - cy) * depth_values / focal_length
    point_cloud[:, 2] = depth_values
    point_cloud = point_cloud[depth_values < 1000]
    colors = rgb[i].reshape(-1, 3)  # Reshape dell'immagine RGB in un array di colori
    colors = colors[depth_values < 1000]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)
    ply.append(pcd)

blender_pose = [[1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1]]

poses2 = []
for pose in tqdm(poses, desc="Trasformazione delle pose in sistema di riferimento di opencv"):
    poses2.append(np.dot(pose, blender_pose))


merged_points = {}
counter = 0 
# Iterazione sui punti della nuvola di punti
for i, pcd in tqdm(enumerate(ply), desc="Trasformazione dei punti e mantenimento traccia"):
    # Trasformazione dei punti
    transformed_pcd = pcd.transform(np.linalg.inv(poses2[0]) @ poses2[i])
    points = np.asarray(transformed_pcd.points)
    
    # Iterazione sui punti trasformati
    for point in points:
        # Arrotondamento delle coordinate del punto a 5 cifre decimali
        rounded_point = tuple(round(coord, 4) for coord in point)
        key = rounded_point
        
        # Verifica se il punto è già presente nel dizionario
        if key not in merged_points:
            merged_points[key] = i
        else:
            counter += 1

print("counter ", counter)
# Creazione della nuvola di punti fusi
merged_pcd = o3d.geometry.PointCloud()
merged_pcd.points = o3d.utility.Vector3dVector(np.array(list(merged_points.keys())))
o3d.visualization.draw_geometries([merged_pcd])
print("4")