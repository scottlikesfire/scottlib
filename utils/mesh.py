# This module contains functions to process and manipulate 3D meshes including file I/O
# the underlying file representation is a simple list of vertices and faces, along with optional 
# vertex normals, UV coordinates, and teture images'
import numpy as np 

def write_obj(verts, faces, filename):
    """
    Write a mesh to an OBJ file. Faces may be any-sized polygons (triangles,
    quads, n-gons) and may have variable size from face to face.

    Parameters:
    verts : ndarray
        Array of vertices (Nx3).
    faces : iterable
        Iterable of faces. Each face is an iterable of vertex indices of any
        length >= 3. Can be a 2D ndarray (uniform size), a list of lists, or
        an object ndarray.
    filename : str
        Output filename.
    """
    with open(filename, 'w') as f:
        for v in verts:
            f.write(f'v {v[0]} {v[1]} {v[2]}\n')
        for face in faces:
            indices = ' '.join(str(int(idx) + 1) for idx in face)
            f.write(f'f {indices}\n')


def read_obj(filename):
    """
    Read a mesh from an OBJ file. Supports faces of any polygon size and the
    'v', 'v/vt', 'v//vn', and 'v/vt/vn' face-corner formats (only the vertex
    index is kept).

    Parameters:
    filename : str
        Input filename.

    Returns:
    verts : ndarray
        Array of vertices (Nx3).
    faces : ndarray
        If every face has the same size, a 2D ndarray of shape (M, K).
        Otherwise an object ndarray of length M whose entries are int lists,
        so mixed-polygon meshes round-trip correctly.
    """
    verts = []
    faces = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                verts.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                parts = line.split()[1:]
                # Each part may be 'v', 'v/vt', 'v//vn', or 'v/vt/vn'.
                face = [int(p.split('/')[0]) - 1 for p in parts]
                faces.append(face)

    if faces and all(len(f) == len(faces[0]) for f in faces):
        faces_arr = np.array(faces, dtype=int)
    else:
        faces_arr = np.array(faces, dtype=object)
    return np.array(verts), faces_arr


def write_stl(verts, faces, filename):
    """
    Write a triangle mesh to a binary STL file.

    Parameters:
    verts : ndarray
        Array of vertices (Nx3).
    faces : ndarray
        Array of faces (Mx3), each row is three vertex indices.
    filename : str
        Output filename.
    """
    import numpy as np
    import struct

    triangles = verts[faces]  # (M, 3, 3)
    v0, v1, v2 = triangles[:, 0], triangles[:, 1], triangles[:, 2]
    normals = np.cross(v1 - v0, v2 - v0)
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    lengths[lengths == 0] = 1.0
    normals /= lengths

    with open(filename, 'wb') as f:
        f.write(b'\0' * 80)  # header
        f.write(struct.pack('<I', len(faces)))
        for i in range(len(faces)):
            f.write(struct.pack('<3f', *normals[i]))
            f.write(struct.pack('<3f', *v0[i]))
            f.write(struct.pack('<3f', *v1[i]))
            f.write(struct.pack('<3f', *v2[i]))
            f.write(struct.pack('<H', 0))  # attribute byte count

def read_stl(filename): 
    """
    Read a triangle mesh from a binary STL file.

    Parameters:
    filename : str
        Input filename.

    Returns:
    verts : ndarray
        Array of vertices (Nx3).
    faces : ndarray
        Array of faces (Mx3), each row is three vertex indices.
    """
    import numpy as np
    import struct

    with open(filename, 'rb') as f:
        f.read(80)  # header
        num_triangles = struct.unpack('<I', f.read(4))[0]
        verts = []
        faces = []
        for i in range(num_triangles):
            f.read(12)  # normal vector
            v0 = struct.unpack('<3f', f.read(12))
            v1 = struct.unpack('<3f', f.read(12))
            v2 = struct.unpack('<3f', f.read(12))
            verts.extend([v0, v1, v2])
            faces.append([len(verts) - 3, len(verts) - 2, len(verts) - 1])
            f.read(2)  # attribute byte count
    return np.array(verts), np.array(faces)

# write pointcloud to ply
def write_ply(points, colors, output_file):
    with open(output_file, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {points.shape[0]}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\n")
        f.write("end_header\n")
        for p, c in zip(points, colors):
            f.write(f"{p[0]} {p[1]} {p[2]} {c[0]} {c[1]} {c[2]}\n")
    

def read_ply(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    header_ended = False
    points = []
    colors = []
    for line in lines:
        if line.strip() == "end_header":
            header_ended = True
            continue
        if not header_ended:
            continue
        parts = line.split()
        if len(parts) < 6:
            continue
        points.append([float(parts[0]), float(parts[1]), float(parts[2])])
        colors.append([int(parts[3]), int(parts[4]), int(parts[5])])
    return np.array(points), np.array(colors)