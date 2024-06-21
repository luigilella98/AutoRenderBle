import math 
import numpy as np 
import matplotlib.pyplot as plt

#rubbishbin
startingmtx = np.array([
    [-0.9392, -0.2955, 0.1748, 0.1372],
    [0.3095, -0.5082, 0.8037, 0.4843],
    [-0.1487, 0.8089, 0.5688, 0.5104],
    [0.0000, 0.0000, 0.0000, 1.0000]
])

#plastic stool
startingmtx =np.array([
     [0.365, 0.4779, -0.799, 0.4853],
     [0.9193, -0.3205, 0.2284, -0.1657],
     [-0.1469, -0.8179, -0.5563, 0.5041],
     [0, 0, 0, 1]

])

#wicker_vase
startingmtx =np.array([
     [-0.8653, 0.4559, -0.2082, 0.1629],
     [0.4674, 0.5843, -0.6634, 0.4083],
     [-0.1809, -0.6714, -0.7187, 0.526],
     [0, 0, 0, 1]

])

startingmtx = np.array([
     [0.5160, -0.4919, 0.7013, 0.5799],
     [0.8417, 0.4430, -0.3086, -0.1987],
     [-0.1589, 0.7495, 0.6426, 0.6868],
     [0,0,0,1]
])

blender_pose = np.array([[1, 0, 0, 0],
                         [0, -1, 0, 0],
                         [0, 0, -1, 0],
                         [0, 0, 0, 1]])

start_ocv = np.dot(startingmtx, blender_pose)
#start_ocv = startingmtx
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



#CALCOLO CIRCONFERENZA 2
#######################
######################
####################
#######################


def move_point_on_sphere(x, y, z, degrees_up):
    # Calcola le coordinate sferiche del punto
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan2(y, x)
    phi = np.arccos(z / r)  # Angolo rispetto all'asse z

    # Aggiungi gradi verso l'alto (phi cresce da 0 a pi)
    new_phi = phi - np.radians(degrees_up)

    # Assicura che new_phi rimanga nel range valido [0, pi]
    new_phi = np.clip(new_phi, 0, np.pi)

    # Calcola le nuove coordinate cartesiane
    new_x = r * np.sin(new_phi) * np.cos(theta)
    new_y = r * np.sin(new_phi) * np.sin(theta)
    new_z = r * np.cos(new_phi)

    return new_x, new_y, new_z
degreeup = 2
starting_point[0], starting_point[1], starting_point[2] = move_point_on_sphere(starting_point[0], starting_point[1], starting_point[2], degreeup)
print("C2 -> st", starting_point)

Rx = rotation_matrix_x(np.radians(-degreeup))
allrotmtx = [starting_rot@Rx]

for _ in range(44):
    new_rot = allrotmtx[-1]@R_z
    allrotmtx.append(new_rot)


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

c2 = ex_lis






#CALCOLO C3
#################
################
####################

degreeup = 2
starting_point[0], starting_point[1], starting_point[2] = move_point_on_sphere(starting_point[0], starting_point[1], starting_point[2], degreeup)
Rx = rotation_matrix_x(np.radians(-degreeup*2))
allrotmtx = [starting_rot@Rx]
print("C3 -> st", starting_point)

for _ in range(44):
    new_rot = allrotmtx[-1]@R_z
    allrotmtx.append(new_rot)


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

c3 = ex_lis




output_path =  './resources/poses/pose.txt'

ex_lis = c1 + c2 + c3
i = 0
with open(output_path, "w") as file:

    for extrinsics in ex_lis:
        print(i)
        if i==0 or i == 45 or i ==90:
            extrinsics_string = " ".join(str(value) for row in extrinsics for value in row)
            file.write(extrinsics_string + "\n")
        i = i+1
