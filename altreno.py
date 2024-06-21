import math 
import numpy as np 
import matplotlib.pyplot as plt

#rubbishbin
#startingmtx = np.array([
#    [-0.9392, -0.2955, 0.1748, 0.1372],
#    [0.3095, -0.5082, 0.8037, 0.4843],
#    [-0.1487, 0.8089, 0.5688, 0.5104],
#    [0.0000, 0.0000, 0.0000, 1.0000]
#])

#plastic stool
startingmtx =np.array([
     [0.365, 0.4779, -0.799, 0.4853],
     [0.9193, -0.3205, 0.2284, -0.1657],
     [-0.1469, -0.8179, -0.5563, 0.5041],
     [0, 0, 0, 1]

])



blender_pose = np.array([[1, 0, 0, 0],
                         [0, -1, 0, 0],
                         [0, 0, -1, 0],
                         [0, 0, 0, 1]])

#start_ocv = np.dot(startingmtx, blender_pose)
start_ocv = startingmtx
starting_point = start_ocv[:3,-1] 
starting_rot = start_ocv[:3,:3]

#matice in sistema opencv


def rotation_matrix_z(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])
def rotation_matrix_x(theta):
    return np.array([
        
        [1, 0, 0],
        [0,np.cos(theta),-np.sin(theta)],
        [0,np.sin(theta), np.cos(theta)]
    ])

def rotation_matrix_y(theta):
     return np.array([
          [np.cos(theta), 0, np.sin(theta)],
          [0,1,0],
          [-np.sin(theta), 0, np.cos(theta)]
     ])

angle_degrees = 8
angle_radians = np.radians(angle_degrees)

R_z = rotation_matrix_z(angle_radians)



allrotmtx = [starting_rot]

# Genera le nuove matrici di rotazione
for _ in range(44):
    new_rot = R_z@allrotmtx[-1]
    allrotmtx.append(new_rot)


def cartesian_to_polar(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta

def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

def point_on_circle(x, y, angle_degrees):
    # Conversione delle coordinate cartesiane in polari
    r, theta = cartesian_to_polar(x, y)

    # Aggiungi l'angolo desiderato
    theta += math.radians(angle_degrees)

    # Converti le coordinate polari risultanti in cartesiane
    new_x, new_y = polar_to_cartesian(r, theta)
    return new_x, new_y

print("C1 -> st", starting_point)
punti = [(starting_point[0], starting_point[1])]

for i in range(45):  # 1 punto di partenza + 44 punti distanti 8 gradi
        new_x, new_y = point_on_circle(punti[0][0], punti[0][1], (i+1) * 8)
        punti.append( (new_x, new_y))

pos = [[punti[i][0], punti[i][1], starting_point[2]] for i in range(len(punti))]


ex_lis = []
for rotation_matrix, position in zip(allrotmtx, pos):
    extrinsics = np.eye(4)
    extrinsics[:3, :3] = rotation_matrix
    extrinsics[:3, -1] = position
    ex_lis.append(extrinsics)


c1 = ex_lis


radius = math.sqrt(starting_point[0]**2+starting_point[1]**2+starting_point[2]**2)
