import argparse
import os
import subprocess
import sys
import cv2 #python -m pip install opencv-python



parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, default='./resources/meshes/', help='path to the folder containing the meshes')
parser.add_argument('--output_path', type=str, default='./renders/', help='path to the folder where the renders will be stored')
parser.add_argument("--template_path", dest='path_template', type=str, default="./resources/Template.blend", help="empty blender template file")
parser.add_argument("--template_path_gt", dest='path_template_gt', type=str, default="./resources/Template_gt.blend", help="empty blender template file fro the gt")
parser.add_argument("--blender_path", type=str, default='C:/Program Files/Blender Foundation/Blender 4.0/blender.exe', help ="path to blender exe")
parser.add_argument("--gt_path", type=str,default= './resources/mesh_gt/', help='path to the gt')
args=parser.parse_args()

def rendering_process(input_path, output_path):
    if not os.path.exists(args.blender_path):
        print("MISSING BLENDER PATH")
    subprocess.run([args.blender_path, args.path_template, "-b", "--python", "scripts/render_mesh.py", "--", "--output_path", output_path, "--input_path", input_path])

def rendering_gt(gt_path, output_path):
    if not os.path.exists(args.blender_path):
        print("MISSING BLENDER PATH")
    subprocess.run([args.blender_path, args.path_template_gt, "-b", "--python", "scripts/render_gt.py", "--", "--output_path", output_path, "--gt_path", gt_path])


if not os.path.exists(args.output_path):
    os.makedirs(args.output_path)


if os.path.isdir(args.input_path):
    for m in os.listdir(args.input_path):
        if m.endswith(".obj"):
            input_path = os.path.join(args.input_path, m)
            output_path = os.path.join(args.output_path, m.replace(".obj", ""))
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            rendering_process(input_path, output_path)


if os.path.isdir(args.gt_path):
    for m in os.listdir(args.gt_path):
        if m.endswith(".ply"):
            gt_path = os.path.join(args.gt_path, m)
            output_path = os.path.join(args.output_path, m.replace(".ply", "_gt"))
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            rendering_gt(gt_path, output_path)

subprocess.check_call([sys.executable, 'mask_creation.py'])




