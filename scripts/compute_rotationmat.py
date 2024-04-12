import math
import numpy as np

def extrinsics_matrix(position, rotation):
    """
    Crea una matrice dei parametri estrinseci di una camera
    partendo dalla posizione e dalla rotazione.
    
    Args:
        position (tuple): Coordinate (x, y, z) della posizione rispetto all'origine.
        rotation (tuple): Angoli di rotazione (in gradi) lungo gli assi x, y e z.

    Returns:
        numpy.ndarray: Matrice dei parametri estrinseci della camera.
    """
    # Converti gli angoli di rotazione da gradi a radianti
    rotation_rad = np.radians(rotation)
    
    # Crea le matrici di rotazione per gli assi x, y e z
    rot_x = np.array([[1, 0, 0],
                      [0, math.cos(rotation_rad[0]), -math.sin(rotation_rad[0])],
                      [0, math.sin(rotation_rad[0]), math.cos(rotation_rad[0])]])
    
    rot_y = np.array([[math.cos(rotation_rad[1]), 0, math.sin(rotation_rad[1])],
                      [0, 1, 0],
                      [-math.sin(rotation_rad[1]), 0, math.cos(rotation_rad[1])]])
    
    rot_z = np.array([[math.cos(rotation_rad[2]), -math.sin(rotation_rad[2]), 0],
                      [math.sin(rotation_rad[2]), math.cos(rotation_rad[2]), 0],
                      [0, 0, 1]])
    
    # Combina le matrici di rotazione
    rotation_matrix = np.matmul(rot_z, np.matmul(rot_y, rot_x))
    
    # Crea la matrice dei parametri estrinseci
    extrinsics = np.eye(4)
    extrinsics[:3, :3] = rotation_matrix
    extrinsics[:3, -1] = position
    
    return extrinsics

# Esempio di utilizzo della funzione
position = (-50, 3, 23.5)
#position = np.array(position)
rotation = (-65, 13, -275)
#rotation = np.array(rotation)
extrinsics = extrinsics_matrix(position, rotation)
print("Matrice dei parametri estrinseci della camera:")
print(extrinsics)
