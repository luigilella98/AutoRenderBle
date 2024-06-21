import numpy as np
import os

POSE_PATH = './renders/KYRRE/RGB/pose.txt'
OUTPUT_PATH = './renders/KYRRE/RGB/pose_ocv.txt'

# Caricamento delle depthmaps
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

poses = load_poses(POSE_PATH)


blender_pose = [[1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1]]

poses2 = []
for pose in poses:
    poses2.append(np.dot(pose, blender_pose))

def save_poses(poses, output_path):
    with open(output_path, 'w') as file:
        for pose in poses:
            pose_flat = pose.flatten()
            pose_string = ' '.join(map(str, pose_flat))
            file.write(pose_string + '\n')

save_poses(poses2, OUTPUT_PATH)