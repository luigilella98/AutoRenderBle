import math
import numpy as np

def extrinsics_matrix(position, rotation):

    
    rotation_rad = np.radians(rotation)
    
    
    rot_x = np.array([[1, 0, 0],
                      [0, math.cos(rotation_rad[0]), -math.sin(rotation_rad[0])],
                      [0, math.sin(rotation_rad[0]), math.cos(rotation_rad[0])]])
    
    rot_y = np.array([[math.cos(rotation_rad[1]), 0, math.sin(rotation_rad[1])],
                      [0, 1, 0],
                      [-math.sin(rotation_rad[1]), 0, math.cos(rotation_rad[1])]])
    
    rot_z = np.array([[math.cos(rotation_rad[2]), -math.sin(rotation_rad[2]), 0],
                      [math.sin(rotation_rad[2]), math.cos(rotation_rad[2]), 0],
                      [0, 0, 1]])
    
    
    rotation_matrix = np.matmul(rot_z, np.matmul(rot_y, rot_x))
    
    extrinsics = np.eye(4)
    extrinsics[:3, :3] = rotation_matrix
    extrinsics[:3, -1] = position
    
    return extrinsics


position = (-50, 3, 23.5)
rotation = (-65, 13, -275)

#position = (42, 34, 15)
#rotation = (73.159, 0, -230.75)

#position = (-50, 3, 23.5)
#rotation = (-65, 13, -275)
extrinsics = extrinsics_matrix(position, rotation)

print("Matrice dei parametri estrinseci della camera:")
print(extrinsics)
