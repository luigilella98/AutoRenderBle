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
    
    # Creazione del point cloud
    point_cloud = np.zeros((mesh_points.shape[0], 3))
    point_cloud[:, 0] = (mesh_points[:, 0] - cx) * depth_values / focal_length
    point_cloud[:, 1] = (mesh_points[:, 1] - cy) * depth_values / focal_length
    point_cloud[:, 2] = depth_values
    valid_points_mask = depth_values < 1000
    point_cloud = point_cloud[valid_points_mask]
    
    # Reshape dell'immagine RGB in un array di colori e applicazione della maschera
    colors = rgb[i].reshape(-1, 3)
    colors = colors[valid_points_mask]
    
    # Creazione del PointCloud Open3D
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)
    
    # Downsampling voxel
    voxel_size = 0.005  # Imposta la dimensione del voxel come necessario
    pcd_downsampled = pcd.voxel_down_sample(voxel_size)
    
    ply.append(pcd_downsampled)

blender_pose = [[1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1]]

poses2 = []
for pose in tqdm(poses, desc="Trasformazione delle pose in sistema di riferimento di opencv"):
    poses2.append(np.dot(pose, blender_pose))


merged_points = {}
discarded_colors = {}
# Creazione di un dizionario per tenere traccia dei colori dei punti scartati durante l'arrotondamento

# Iterazione sui punti della nuvola di punti
for i, pcd in tqdm(enumerate(ply), desc="Trasformazione dei punti e mantenimento traccia"):
    # Trasformazione dei punti
    transformed_pcd = pcd.transform(np.linalg.inv(poses2[0]) @ poses2[i])
    points = np.asarray(transformed_pcd.points)
    colors = np.asarray(transformed_pcd.colors) * 255.0  # Moltiplica per 255 per ottenere valori di colore in scala 0-255
    
    # Iterazione sui punti trasformati
    for j, point in enumerate(points):
        # Arrotondamento delle coordinate del punto a 4 cifre decimali
        key = tuple(round(coord, 4) for coord in point)
        
        
        # Verifica se il punto è già presente nel dizionario
        if key not in merged_points:
            # Se il punto non è presente, aggiungi il suo colore al dizionario dei colori scartati
            discarded_colors[key] = [colors[j]]
            merged_points[key] = i
        else:
            # Se il punto è già presente, aggiungi il colore al dizionario dei colori scartati
            discarded_colors[key].append(colors[j])
            

# Creazione della nuvola di punti fusi con i colori medi

del ply
del depth
del rgb
del poses


merged_pcd = o3d.geometry.PointCloud()
merged_points_list = np.array(list(merged_points.keys()))
merged_points_list_flat = merged_points_list.reshape(-1, 3)
print("LENGTH", len(merged_points_list_flat))
merged_pcd.points = o3d.utility.Vector3dVector(merged_points_list_flat)

del merged_points_list_flat
del merged_points


merged_colors = []

# Calcolo dei colori medi per i punti con le stesse coordinate
for point in tqdm(merged_points_list, desc='colorazione'):
    # Converti l'array NumPy in una tupla
    point_tuple = tuple(point)
    merged_colors.append(np.mean(discarded_colors[point_tuple], axis=0))

# Reshape delle coordinate in un array monodimensionale di vettori 3D

merged_colors = np.array(merged_colors)
# Assegnazione delle coordinate e dei colori alla nuvola di punti fusi

merged_pcd.colors = o3d.utility.Vector3dVector(merged_colors / 255.0)

# Visualizzazione della nuvola di punti fusi

mesh_path = './prove/MAMMUT.glb'  # Assicurati di inserire il percorso corretto al file della mesh GLB
mesh = o3d.io.read_triangle_mesh(mesh_path)

# Trasforma la mesh nello stesso sistema di riferimento della nuvola di punti utilizzando le pose
transformed_mesh = mesh.transform(np.linalg.inv(poses2[0]))

# Visualizza la mesh e la nuvola di punti fusa
o3d.visualization.draw_geometries([merged_pcd, transformed_mesh])

