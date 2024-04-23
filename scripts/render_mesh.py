import bpy
import sys
import argparse
import os
import numpy as np
import xml.etree.ElementTree as ET

PATH_POSE = './resources/poses/pose.txt'
PATH_CALIB = './resources/calib.xml'

RESX = 4090
RESY = 3126

if '--' in sys.argv:
    argv = sys.argv[sys.argv.index('--') + 1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_path', type=str, default='./renders/', help='path to the folder where the renders will be stored')
    parser.add_argument('--input_path', type=str, default='./resources/meshes/', help='path to the folder containing the meshes')

    args=parser.parse_known_args(argv)[0]

def read_pose(line):
    splits = line.split(" ")
    pose=np.zeros([4,4])
    pose[3,3]=1
    for idx,s in enumerate(splits):
        pose[idx//4, idx%4]=float(s)
    return pose

def read_intrinsics(path_c):
    tree = ET.parse(path_c)
    root = tree.getroot()

    mtxL = root.find(".//mtxL")
    data = mtxL.find('data').text.split()
    
    fkx = float(data[0])
    x0 = float(data[2])
    fky = float(data[4])
    y0 = float(data[5])

    return fkx, x0, fky, y0

def setCameraParams(cam, fkx, fky, x0, y0):
    pixel2mm = cam.sensor_width/RESX
    cam.type = 'PERSP'
    cam.lens = fkx*pixel2mm
    cam.lens_unit = 'MILLIMETERS'
    cam.shift_x = (RESX/2 - x0)/RESX
    cam.shift_y = (RESY/2 - y0)/RESY
    cam.clip_start = 0.01
    cam.clip_end = 5000

extrinsics = open(PATH_POSE).readlines()
fkx, x0, fky, y0 = read_intrinsics(PATH_CALIB)


bpy.ops.import_scene.gltf(filepath = args.input_path) #sostituire in base al tipo di file
bpy.context.scene.render.engine = 'CYCLES'
bpy.data.scenes["Scene"].cycles.device = 'GPU'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.resolution_x = RESX
bpy.context.scene.render.resolution_y = RESY    

cam_obj=bpy.data.objects["Camera"]
cam=bpy.data.cameras["Camera"]
bpy.data.scenes["Scene"].camera=cam_obj
setCameraParams(cam, fkx, fky, x0, y0)


for idx,pose in enumerate(extrinsics):
    matx = read_pose(pose)
    matx = np.transpose(matx,axes=[1,0])
    cam_obj.matrix_world = matx
    bpy.data.scenes["Scene"].render.filepath = os.path.join(os.path.abspath(args.output_path),"posa_{:03d}".format(idx))
    bpy.ops.render.render(write_still=True)