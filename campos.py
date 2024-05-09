import open3d as o3d
import numpy as np

# Funzione per visualizzare le pose della camera
def visualize_camera_poses(poses):
    geometries = []

    # Crea una griglia per rappresentare l'asse delle coordinate
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.6)

    # Aggiungi la griglia a geometries
    geometries.append(mesh_frame)

    # Crea una freccia per rappresentare la direzione dello sguardo della camera
    camera_direction_arrow = o3d.geometry.TriangleMesh.create_arrow(cylinder_radius=0.05, cone_radius=0.1, cylinder_height=0.5, cone_height=0.3)
    camera_direction_arrow.compute_vertex_normals()

    for pose in poses:
        # Crea una copia della freccia per ogni posa
        arrow_copy = o3d.geometry.TriangleMesh(camera_direction_arrow)

        # Applica la trasformazione della posa alla freccia
        arrow_copy.transform(pose)

        # Aggiungi la freccia trasformata a geometries
        geometries.append(arrow_copy)

    # Visualizza le geometrie
    o3d.visualization.draw_geometries(geometries)

# Carica le pose delle camere dal file
def load_poses(posepath):
    pose = open(posepath).readlines()
    poses = []
    for line in pose:
        splits = line.split(" ")
        mtx = np.zeros([4, 4])
        mtx[3, 3] = 1
        for idx, s in enumerate(splits):
            mtx[idx // 4, idx % 4] = float(s)
        poses.append(mtx)
    return poses

# Percorso del file contenente le pose delle camere
POSE_PATH = './prove/pose.txt'

# Carica le pose delle camere
poses = load_poses(POSE_PATH)

# Matrice di trasformazione di Blender
blender_pose = np.array([[1, 0, 0, 0],
                         [0, -1, 0, 0],
                         [0, 0, -1, 0],
                         [0, 0, 0, 1]])

# Applica la trasformazione di Blender alle pose delle camere
poses2 = [np.dot( pose, blender_pose) for pose in poses]

# Visualizza le pose della camera
visualize_camera_poses(poses2)
