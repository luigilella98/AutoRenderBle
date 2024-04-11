import argparse
import os
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, default='./resources/meshes/', help='path to the folder containing the meshes')
parser.add_argument('--output_path', type=str, default='./renders/', help='path to the folder where the renders will be stored')
parser.add_argument("--template_path", dest='path_template', type=str, default="./resources/template.blend", help="empty blender template file")
parser.add_argument("--blender_path", type=str, default='C:/Program Files/Blender Foundation/Blender 4.0/blender.exe', help ="path to blender exe")
args=parser.parse_args()

def rendering_process(input_path, output_path):
    if not os.path.exists(args.blender_path):
        print("MISSING BLENDER PATH")
    subprocess.run([args.blender_path, args.path_template, "-b", "--python", "scripts/render_mesh.py", "--", "--output_path", output_path, "--input_path", input_path])


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
