import argparse
import math
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('--output_pose', type=str, default='./resources/poses/', help='path to the folder where the pose.txt will be stored')
parser.add_argument("--radius", type=float, default=1.0, help ="radius of the sphere")
parser.add_argument("--step", type=float, default=0.15, help="step along z")
parser.add_argument("--num_pose", type=int, default=12, help="number of poses that will be generated")

args=parser.parse_args()

alpha = [(2*math.pi)/(args.num_pose)*a for a in range(args.num_pose)]
theta = [math.acos((i*args.step)/args.radius)for i in range(1,4)]

c_1 = [(args.radius*math.sin(theta[0])*math.cos(a), args.radius*math.sin(theta[0])*math.sin(a), args.step*1) for a in alpha]
c_2 = [(args.radius*math.sin(theta[1])*math.cos(a), args.radius*math.sin(theta[1])*math.sin(a), args.step*2) for a in alpha]
c_3 = [(args.radius*math.sin(theta[2])*math.cos(a), args.radius*math.sin(theta[2])*math.sin(a), args.step*3) for a in alpha]

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

#creatrion rotation tuple 
def rot_lista(points):
    return [(math.degrees(math.atan2(math.dist((p[0],p[1]),(0,0)), p[2])),0,math.degrees(np.arctan2(p[1], p[0]) + math.pi/2)) for p in points]

c1_rot = rot_lista(c_1)
c2_rot = rot_lista(c_2)
c3_rot = rot_lista(c_3)

points = c_1 + c_2 + c_3
rots = c1_rot + c2_rot + c3_rot

extrinsics_list = []
for pos, rot in zip(points, rots):
    extrinsics_list.append(extrinsics_matrix(pos, rot))

nome_file = './resources/poses/pose.txt'

with open(nome_file, "w") as file:

    for matrice in extrinsics_list:

        matrice_stringa = " ".join(str(valore) for riga in matrice for valore in riga)

        file.write(matrice_stringa + "\n")