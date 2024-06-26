import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import cv2
import numpy as np
import open3d as o3d
import tifffile

# Carica la depth map
depth_map = cv2.imread('C:/Users/luigi/Desktop/posa_000_depth.exr', cv2.IMREAD_UNCHANGED)
print(depth_map.min(), depth_map.max())
print(type(depth_map[0,0][0]))

import matplotlib.pyplot as plt
plt.imshow(depth_map[:,:,0])
plt.show()

# Parametri della fotocamera
focal_length = 3.4702761957637335e+03  # Focale della tua telecamera
cx = 2.0457960174875925e+03
cy = 1.5636291650560495e+03  # Centro dell'immagine (pixel)

# Calcola la point cloud
h, w = depth_map.shape[:2]
mesh_x, mesh_y = np.meshgrid(range(w), range(h))
mesh_points = np.dstack((mesh_x, mesh_y)).reshape(-1, 2)
depth_values = depth_map[:, :, 0].reshape(-1)
point_cloud = np.zeros((mesh_points.shape[0], 3))
point_cloud[:, 0] = (mesh_points[:, 0] - cx) * depth_values / focal_length
point_cloud[:, 1] = (mesh_points[:, 1] - cy) * depth_values / focal_length
point_cloud[:, 2] = depth_values

xyz = point_cloud.reshape([h,w,3])
xyz[depth_map[:,:,0] > 100] = [0, 0, 0]

plt.imshow(xyz)
plt.show()
#cv2.imwrite('xyz_nocompression.tiff',xyz) #risultato troppo pesante
#cv2.imwrite('xyz_32bit.tiff',xyz.astype(np.float32)) #risultato non consistente
#cv2.imwrite('xyz_5.tiff', xyz, params=(cv2.IMWRITE_TIFF_COMPRESSION, 5)) #compressione LZW, dovrebbe essere quella di
#cv2.imwrite('xyz_adobe.tiff', xyz, (cv2.IMWRITE_TIFF_COMPRESSION, 8)) #compressione adobe deflate
#cv2.imwrite('xyz_deflate.tiff', xyz, (cv2.IMWRITE_TIFF_COMPRESSION, 32956)) #deflate

#tifffile.imwrite('tif_xyz.tiff', xyz, compression='zlib')

# Inverti l'asse y per adattarlo al sistema di riferimento della fotocamera
#point_cloud[:, 1] *= -1

# Rimuovi i punti con profondità zero (valori non validi)
point_cloud = point_cloud[depth_values < 1000]

# Visualizza la point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud)
o3d.visualization.draw_geometries([pcd])
#pcd.estimate_normals()

#mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha=0.1)

# Visualizza la mesh
#o3d.visualization.draw_geometries([mesh])
#print("FATTO")
#o3d.io.write_point_cloud("my_pts2.ply", pcd)