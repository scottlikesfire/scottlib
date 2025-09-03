# This module contains functions to process and manipulate 3D meshes including file I/O
# the underlying file representation is a simple list of vertices and faces, along with optional 
# vertex normals, UV coordinates, and teture images'

# This is no good but im doing it for now. it only supports triangles
def write_obj(verts, faces, filename):
    """
    Write a point cloud to an OBJ file.
    
    Parameters:
    verts : ndarray
        Array of vertices (Nx3).
    faces : ndarray
        Array of faces (Mx3).
    filename : str
        Output filename.
    """
    with open(filename, 'w') as f:
        for v in verts:
            f.write(f'v {v[0]} {v[1]} {v[2]}\n')
        for face in faces:
            f.write(f'f {face[0]+1} {face[1]+1} {face[2]+1}\n')

# write pointcloud to ply
def write_to_ply(points, colors, output_file):
    with open(output_file, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {points.shape[0]}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\n")
        f.write("end_header\n")
        for p, c in zip(points, colors):
            f.write(f"{p[0]} {p[1]} {p[2]} {c[0]} {c[1]} {c[2]}\n")
    