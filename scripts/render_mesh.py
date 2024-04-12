import bpy
import sys
import argparse
import os
import numpy as np

path_pose = './resources/poses/pose.txt'

if '--' in sys.argv:
    argv = sys.argv[sys.argv.index('--') + 1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_path', type=str, default='./renders/', help='path to the folder where the renders will be stored')
    parser.add_argument('--input_path', type=str, default='./resources/meshes/', help='path to the folder containing the meshes')

    args=parser.parse_known_args(argv)[0]

def decode_pose(line):
    splits = line.split(" ")
    pose=np.zeros([4,4])
    pose[3,3]=1
    for idx,s in enumerate(splits):
        pose[idx//4, idx%4]=float(s)
    return pose

extrinsics = open(path_pose).readlines()
bpy.ops.wm.obj_import(filepath = args.input_path)
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
cam_obj=bpy.data.objects["Camera"]

for idx,pose in enumerate(extrinsics):
    mat = decode_pose(pose)
    mat=np.transpose(mat,axes=[1,0])
    cam_obj.matrix_world = mat
    bpy.data.scenes["Scene"].render.filepath = os.path.join(os.path.abspath(args.output_path),"{:010d}".format(idx))
    bpy.ops.render.render(write_still=True)

