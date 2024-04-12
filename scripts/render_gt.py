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
    parser.add_argument('--gt_path', type=str, default='./resources/mesh_gt/', help='path to the folder containing the gt')

    args=parser.parse_known_args(argv)[0]

def decode_pose(line):
    splits = line.split(" ")
    pose=np.zeros([4,4])
    pose[3,3]=1
    for idx,s in enumerate(splits):
        pose[idx//4, idx%4]=float(s)
    return pose

def assign_mat(obj):
    material = bpy.data.materials.new(name='gt_material')
    material.use_nodes = True

    # Ottieni il nodo Principled BSDF
    principled_bsdf_node = material.node_tree.nodes.get("Principled BSDF")

# Aggiungi un nodo ShaderNodeAttribute per l'attributo "Col"
    attribute_node = material.node_tree.nodes.new('ShaderNodeAttribute')
    attribute_node.attribute_name = "Col"  # Imposta l'attributo su "Col"
    attribute_node.location = (-200, 0)  # Imposta la posizione del nodo

# Aggiungi un nodo ShaderNodeOutputMaterial
    output_node = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (400, 0)  # Imposta la posizione del nodo

# Collega il nodo ShaderNodeAttribute al colore di base del nodo Principled BSDF
    material.node_tree.links.new(attribute_node.outputs['Color'], principled_bsdf_node.inputs['Base Color'])

# Collega il nodo Principled BSDF al nodo ShaderNodeOutputMaterial  
    material.node_tree.links.new(principled_bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])


# Assegna il materiale all'oggetto trovato
    if obj:
        if obj.data.materials:
        # Se l'oggetto ha già dei materiali assegnati, sostituisci il primo materiale con quello creato
            obj.data.materials[0] = material
        else:
        # Altrimenti, aggiungi il materiale alla lista dei materiali dell'oggetto
            obj.data.materials.append(material)
    else:
        print("Nessun oggetto con il nome trovato nella scena.")


extrinsics = open(path_pose).readlines()

bpy.ops.wm.ply_import(filepath = args.gt_path)

assign_mat(bpy.data.objects[args.gt_path[args.gt_path.rfind('/') + 1 :args.gt_path.rfind('.')]])
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