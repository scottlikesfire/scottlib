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