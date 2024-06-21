import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import cv2
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from tqdm import tqdm

DEPTH_PATH = './renders/NOJIG/depth'
RGB_PATH = './renders/NOJIG/rgb'
POSE_PATH = './renders/NOJIG/RGB/pose.txt'

# Caricamento delle depthmaps
def load_depth(dpath):
    depths = []
    if os.path.isdir(dpath):
        for f in tqdm(os.listdir(dpath), desc="Caricamento delle depthmaps"):
            if not f.endswith("txt"):
                depths.append(cv2.imread(os.path.join(dpath, f), cv2.IMREAD_UNCHANGED))
    return depths

# Caricamento delle RGBs
def load_rgbs(rgbpath):
    rgbs = []
    if os.path.isdir(rgbpath):
        for f in tqdm(os.listdir(rgbpath), desc="Caricamento delle RGBs"):
            if not f.endswith("txt"):
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

focal_length = 3.4702761957637335e+03  
cx = 2.0457960174875925e+03
cy = 1.5636291650560495e+03 

depth = load_depth(DEPTH_PATH)
rgb = load_rgbs(RGB_PATH)
poses = load_poses(POSE_PATH)

ply = []

# Creazione delle pc dalle depth
for i in tqdm(range(len(depth)), desc="Creazione delle pointcloud"):
    h, w = depth[i].shape[:2]
    mesh_x, mesh_y = np.meshgrid(range(w), range(h))
    mesh_points = np.dstack((mesh_x, mesh_y)).reshape(-1, 2)
    depth_values = depth[i][:, :, 0].reshape(-1)
    

    point_cloud = np.zeros((mesh_points.shape[0], 3))
    point_cloud[:, 0] = (mesh_points[:, 0] - cx) * depth_values / focal_length
    point_cloud[:, 1] = (mesh_points[:, 1] - cy) * depth_values / focal_length
    point_cloud[:, 2] = depth_values
    points_mask = depth_values < 1000
    point_cloud = point_cloud[points_mask]
    

    colors = rgb[i].reshape(-1, 3)
    colors = colors[points_mask]
    

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)
    

    voxel_size = 0.008  
    pcd_down = pcd.voxel_down_sample(voxel_size)
    
    ply.append(pcd_down)

# da togliere, modificare il file delle pose, modificare il file di rendering per adattarsi , lascia con un if
blender_pose = [[1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1]]

poses2 = []
for pose in tqdm(poses, desc="sdr blender -> ocv"):
    poses2.append(np.dot(pose, blender_pose))


merged_pcd = o3d.geometry.PointCloud()

for i, pcd in tqdm(enumerate(ply), desc="Pointcloud portate rispetto la stessa posa"):

    transformed_pcd = pcd.transform(np.linalg.inv(poses2[0]) @ poses2[i]) #nella mia testa era al contrario anche eyecandies mette prima inv
    merged_pcd += transformed_pcd

# Caricamento mesh
mesh = o3d.io.read_triangle_mesh("./prove/fbx/NOJIG.fbx")

#rotation_matrix = mesh.get_rotation_matrix_from_axis_angle(( np.pi/2, 0,0))
#mesh.rotate(rotation_matrix)

# allineamento a pointcloud
mesh.transform(np.linalg.inv(poses2[0]))

o3d.visualization.draw_geometries([merged_pcd, mesh])


# assegnazione dei colori 
k = 6  
pcd_tree = o3d.geometry.KDTreeFlann(merged_pcd)
colors = np.asarray(merged_pcd.colors)


mesh_vertex_colors = np.zeros((len(mesh.vertices), 3))

for i, vertex in enumerate(tqdm(mesh.vertices, desc="Assegnazione dei colori ai vertici della mesh")):
    [_, idx, _] = pcd_tree.search_knn_vector_3d(vertex, k)
    nearest_colors = colors[idx]
    mesh_vertex_colors[i] = np.mean(nearest_colors, axis=0)


mesh.vertex_colors = o3d.utility.Vector3dVector(mesh_vertex_colors)

o3d.visualization.draw_geometries([mesh])