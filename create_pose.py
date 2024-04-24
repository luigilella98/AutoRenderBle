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

'''
x = -0.4465142774872936
y = 0.7733854149129011
z = 0.44999999999999996

rot_z = np.arctan2(y, x) + math.pi/2
rot_x = math.atan2(z,y) + math.pi/2
'''
for p in c_1:
    print(p)
    print(math.degrees(math.atan2(math.dist((p[0],p[1]),(0,0)), p[2])))
    print(math.degrees(np.arctan2(p[1], p[0]) + math.pi/2))
    
