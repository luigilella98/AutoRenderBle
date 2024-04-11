import bpy
import sys
import argparse
import os

if '--' in sys.argv:
    argv = sys.argv[sys.argv.index('--') + 1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_path', type=str, default='./renders/', help='path to the folder where the renders will be stored')
    parser.add_argument('--input_path', type=str, default='./resources/meshes/', help='path to the folder containing the meshes')

    args=parser.parse_known_args(argv)[0]


bpy.ops.wm.obj_import(filepath = args.input_path)
bpy.context.scene.render.image_settings.file_format = 'PNG'


bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.data.scenes["Scene"].render.filepath = os.path.join(os.path.abspath(args.output_path),"name")
bpy.ops.render.render(write_still=True) 