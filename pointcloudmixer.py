import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import cv2
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

# Carica la depth map
depth_map = cv2.imread('C:/Users/luigi/Desktop/posa_000_depth.exr', cv2.IMREAD_UNCHANGED)
print(depth_map.min(), depth_map.max())

# Carica l'immagine RGB
rgb_image = cv2.imread('C:/Users/luigi/Desktop/posa_000.png')

# Visualizza la depth map
plt.imshow(depth_map[:,:,0])
plt.show()

# Parametri della fotocamera
focal_length = 3.4702761957637335e+03  # Focale della tua telecamera
cx = depth_map.shape[1] / 2
cy = depth_map.shape[0] / 2  # Centro dell'immagine (pixel)

# Calcola la point cloud
h, w = depth_map.shape[:2]
mesh_x, mesh_y = np.meshgrid(range(w), range(h))
mesh_points = np.dstack((mesh_x, mesh_y)).reshape(-1, 2)
depth_values = depth_map[:, :, 0].reshape(-1)
point_cloud = np.zeros((mesh_points.shape[0], 3))
point_cloud[:, 0] = (mesh_points[:, 0] - cx) * depth_values / focal_length
point_cloud[:, 1] = (mesh_points[:, 1] - cy) * depth_values / focal_length
point_cloud[:, 2] = depth_values

# Inverti l'asse y per adattarlo al sistema di riferimento della fotocamera
# point_cloud[:, 1] *= -1

# Rimuovi i punti con profondità zero (valori non validi)
point_cloud = point_cloud[depth_values < 1000]

# Estrai i colori corrispondenti ai punti nella nuvola di punti
colors = rgb_image.reshape(-1, 3)  # Reshape dell'immagine RGB in un array di colori
colors = colors[depth_values < 1000]  # Considera solo i colori dei punti validi

# Visualizza la point cloud
xyz = point_cloud.reshape([h,w,3])
plt.imshow(xyz)
plt.show()

# Visualizza la nuvola di punti colorata
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud)
pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Normalizza i colori tra 0 e 1 e assegna alla nuvola di punti
o3d.visualization.draw_geometries([pcd])
