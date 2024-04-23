import argparse
import math

parser = argparse.ArgumentParser()

parser.add_argument('--output_pose', type=str, default='./resources/poses/', help='path to the folder where the pose.txt will be stored')
parser.add_argument("--radius", type=float, default=1.0, help ="radius of the sphere")
parser.add_argument("--step", type=float, default=0, help="step along z")
parser.add_argument("--num_pose", type=int, default=12, help="number of poses that will be generated")

args=parser.parse_args()

alpha = [math.degrees((2*math.pi)/(args.num_pose)*a) for a in range(args.num_pose)]
theta = [math.acos((i*args.step)/args.radius) for i in range(1,4)]

c_1 = [(args.radius*math.sin(theta[0])*math.cos(a), args.radius*math.sin(theta[0])*math.sin(a), args.step) for a in alpha]
c_2 = [(args.radius*math.sin(theta[1])*math.cos(a), args.radius*math.sin(theta[1])*math.sin(a), args.step) for a in alpha]
c_3 = [(args.radius*math.sin(theta[2])*math.cos(a), args.radius*math.sin(theta[2])*math.sin(a), args.step) for a in alpha]

