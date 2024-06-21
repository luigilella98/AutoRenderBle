import open3d as o3d
import numpy as np

# Carica la mesh da un file
mesh = o3d.io.read_triangle_mesh("./resources/KYRRE.glb")
mesh2 = o3d.io.read_triangle_mesh("./prove/fbx/KYRRE.fbx")

# Verifica che la mesh sia caricata correttamente
if not mesh.has_vertices():
    print("Errore: La mesh non contiene vertici.")
else:
    # Assumi che l'origine della mesh sia (0, 0, 0)
    origin = np.array([0, 0, 0])

    # Stampa l'origine della mesh
    print(f"L'origine della mesh è: {origin}")

# Facoltativo: visualizza la mesh e il suo centro
cor = o3d.geometry.TriangleMesh.create_coordinate_frame().scale(0.25, center=(0, 0, 0))
mesh_center = o3d.geometry.TriangleMesh.create_sphere(radius=0.01)
mesh_center.translate(origin)
rotation_matrix = mesh.get_rotation_matrix_from_axis_angle(( -np.pi/2, 0,0))
mesh2.rotate(rotation_matrix)
mesh.paint_uniform_color([0,1,0])

o3d.visualization.draw_geometries([mesh, mesh_center,mesh2, cor])