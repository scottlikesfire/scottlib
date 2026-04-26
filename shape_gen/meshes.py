# This module contains code for generation of some parametric 3D meshes.

import math

import numpy as np
from scottlib.utils import coordinates

# TODO: switch over to coordinates module for all coordinate conversions




def generate_cylinder(radius, height, num_segments):
    """
    Generate a cylinder mesh.
    
    Parameters:
    radius : float
        Radius of the cylinder.
    height : float
        Height of the cylinder.
    num_segments : int
        Number of segments around the cylinder.
        
    Returns:
    vertices : ndarray
        Array of vertices (Nx3).
    faces : ndarray
        Array of faces (Mx3).
    """
    # Generate vertices
    theta = np.linspace(0, 2 * np.pi, num_segments)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.array([0, height])
    # x,y = coordinates.polar2cart(radius, theta)

    
    vertices = np.array([[x[i], y[i], z[j]] for j in range(2) for i in range(num_segments)])
    
    # Generate faces
    faces = []
    for i in range(num_segments):
        next_i = (i + 1) % num_segments
        faces.append([i, next_i, i + num_segments])
        faces.append([next_i, next_i + num_segments, i + num_segments])
    
    # Add top and bottom faces
    v_c0 = np.array([0, 0, 0])
    v_c1 = np.array([0, 0, height])
    vertices = np.concatenate((vertices,v_c0.reshape(1,3),v_c1.reshape(1,3)),axis = 0)
    vc0_ind = num_segments * 2
    vc1_ind = num_segments * 2 + 1

    for i in range(num_segments):
        next_i = (i + 1) % num_segments
        faces.append([vc0_ind, next_i,i])
        faces.append([vc1_ind, i + num_segments, next_i + num_segments])
   
    return vertices, faces

def generate_truncated_cone(radius1,radius2,height,num_segments):
    """
    Generate a truncated cone mesh.
    
    Parameters:
    radius1 : float
        Radius of the bottom circle.
    radius2 : float
        Radius of the top circle.
    height : float
        Height of the cone.
    num_segments : int
        Number of segments around the cone.
        
    Returns:
    vertices : ndarray
        Array of vertices (Nx3).
    faces : ndarray
        Array of faces (Mx3).
    """
    # Generate vertices
    theta = np.linspace(0, 2 * np.pi, num_segments)
    x1 = radius1 * np.cos(theta)
    y1 = radius1 * np.sin(theta)
    z1 = np.array([0])
    
    x2 = radius2 * np.cos(theta)
    y2 = radius2 * np.sin(theta)
    z2 = np.array([height])
    
    vertices = np.array([[x1[i], y1[i], z1[0]] for i in range(num_segments)] + 
                        [[x2[i], y2[i], z2[0]] for i in range(num_segments)])
    
    # Generate faces
    faces = []
    for i in range(num_segments):
        next_i = (i + 1) % num_segments
        faces.append([i, next_i, i + num_segments])
        faces.append([next_i, next_i + num_segments, i + num_segments])

         # Add top and bottom faces
    v_c0 = np.array([0, 0, 0])
    v_c1 = np.array([0, 0, height])
    # import pdb;pdb.set_trace()
    vertices = np.concatenate((vertices,v_c0.reshape(1,3),v_c1.reshape(1,3)),axis = 0)
    vc0_ind = num_segments * 2
    vc1_ind = num_segments * 2 + 1

    for i in range(num_segments):
        next_i = (i + 1) % num_segments
        faces.append([vc0_ind, next_i,i])
        faces.append([vc1_ind, i + num_segments, next_i + num_segments])

    return vertices, faces


# ----- Platonic solids -----

def generate_tetrahedron():
    """Regular tetrahedron inscribed in a unit cube."""
    verts = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
    ], dtype=float)
    faces = [
        [0, 1, 2],
        [0, 3, 1],
        [0, 2, 3],
        [1, 3, 2],
    ]
    return verts, faces


def generate_octahedron():
    """Regular octahedron — 6 verts on the unit axes."""
    verts = np.array([
        [1, 0, 0],   # 0
        [-1, 0, 0],  # 1
        [0, 1, 0],   # 2
        [0, -1, 0],  # 3
        [0, 0, 1],   # 4 (top)
        [0, 0, -1],  # 5 (bottom)
    ], dtype=float)
    faces = [
        # Top fan
        [4, 0, 2], [4, 2, 1], [4, 1, 3], [4, 3, 0],
        # Bottom fan (reverse winding)
        [5, 2, 0], [5, 1, 2], [5, 3, 1], [5, 0, 3],
    ]
    return verts, faces


def generate_icosahedron():
    """Regular icosahedron — 12 verts, 20 triangle faces."""
    phi = (1 + math.sqrt(5)) / 2
    verts = np.array([
        [-1,  phi,  0], [ 1,  phi,  0], [-1, -phi,  0], [ 1, -phi,  0],
        [ 0, -1,   phi], [ 0,  1,   phi], [ 0, -1,  -phi], [ 0,  1,  -phi],
        [ phi, 0, -1], [ phi, 0,  1], [-phi, 0, -1], [-phi, 0,  1],
    ], dtype=float)
    # Normalize so all verts lie on the unit sphere
    verts = verts / np.linalg.norm(verts[0])
    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
    ]
    return verts, faces


def generate_dodecahedron():
    """Regular dodecahedron — 20 verts, 12 pentagonal faces.

    Built as the dual of the icosahedron: dodecahedron vertices are the
    centroids of the icosahedron faces, and each dodecahedron face is the
    cyclically-ordered set of icosahedron faces incident to one icosahedron
    vertex.
    """
    ico_verts, ico_faces = generate_icosahedron()

    # Vertices = normalized icosahedron face centroids
    centroids = []
    for f in ico_faces:
        c = (ico_verts[f[0]] + ico_verts[f[1]] + ico_verts[f[2]]) / 3.0
        centroids.append(c / np.linalg.norm(c))
    centroids = np.array(centroids)

    # Pentagons = cyclic fan of incident icosahedron faces around each vert
    faces = []
    for v in range(len(ico_verts)):
        incident = [i for i, f in enumerate(ico_faces) if v in f]
        ordered = [incident[0]]
        remaining = set(incident[1:])
        while remaining:
            last_face = set(ico_faces[ordered[-1]])
            for nf in list(remaining):
                if len(last_face & set(ico_faces[nf])) == 2:
                    ordered.append(nf)
                    remaining.remove(nf)
                    break
            else:
                break

        # The fan walk's direction is arbitrary, so half the pentagons end
        # up wound the wrong way. Force outward winding: the dodecahedron is
        # centered at the origin, so a face is correctly wound iff its
        # geometric normal points away from the origin.
        c0, c1, c2 = centroids[ordered[0]], centroids[ordered[1]], centroids[ordered[2]]
        normal = np.cross(c1 - c0, c2 - c0)
        face_centroid = np.mean(centroids[ordered], axis=0)
        if np.dot(normal, face_centroid) < 0:
            ordered = list(reversed(ordered))

        faces.append(ordered)
    return centroids, faces


# ----- Solids of revolution / smooth shapes -----

def generate_uv_sphere(radius=1.0, num_lat=6, num_lon=8):
    """UV sphere with z up. num_lat = number of horizontal rings between poles."""
    verts = [[0.0, 0.0, radius]]  # top pole
    for i in range(1, num_lat + 1):
        phi = i * math.pi / (num_lat + 1)
        z = radius * math.cos(phi)
        rr = radius * math.sin(phi)
        for j in range(num_lon):
            theta = j * 2 * math.pi / num_lon
            verts.append([rr * math.cos(theta), rr * math.sin(theta), z])
    verts.append([0.0, 0.0, -radius])  # bottom pole

    top_idx = 0
    bottom_idx = len(verts) - 1
    faces = []
    # Top cap
    for j in range(num_lon):
        a = 1 + j
        b = 1 + (j + 1) % num_lon
        faces.append([top_idx, a, b])
    # Middle quads — wound CCW from outside the sphere so normals point out
    for i in range(num_lat - 1):
        for j in range(num_lon):
            a = 1 + i * num_lon + j
            b = 1 + i * num_lon + (j + 1) % num_lon
            c = 1 + (i + 1) * num_lon + (j + 1) % num_lon
            d = 1 + (i + 1) * num_lon + j
            faces.append([a, d, c, b])
    # Bottom cap
    base = 1 + (num_lat - 1) * num_lon
    for j in range(num_lon):
        a = base + j
        b = base + (j + 1) % num_lon
        faces.append([bottom_idx, b, a])
    return np.array(verts), faces


def generate_torus(major_radius=1.0, minor_radius=0.35, num_major=12, num_minor=6):
    """Torus around the z axis. num_major sweeps around the big ring,
    num_minor segments around the small tube cross-section."""
    verts = []
    for i in range(num_major):
        u = i * 2 * math.pi / num_major
        cu, su = math.cos(u), math.sin(u)
        for j in range(num_minor):
            v = j * 2 * math.pi / num_minor
            cv, sv = math.cos(v), math.sin(v)
            x = (major_radius + minor_radius * cv) * cu
            y = (major_radius + minor_radius * cv) * su
            z = minor_radius * sv
            verts.append([x, y, z])

    faces = []
    for i in range(num_major):
        ip = (i + 1) % num_major
        for j in range(num_minor):
            jp = (j + 1) % num_minor
            a = i * num_minor + j
            b = i * num_minor + jp
            c = ip * num_minor + jp
            d = ip * num_minor + j
            # Wound so the face normal points away from the local tube axis
            faces.append([a, d, c, b])
    return np.array(verts), faces


def generate_trefoil_knot(major_radius=1.0, minor_radius=0.2,
                          num_curve=32, num_ring=4):
    """Trefoil-knot tube using the Frenet frame.

    Parallel transport accumulates twist around the loop, so the last ring
    doesn't line up with the first. The Frenet frame is computed
    independently at each sample from the curve's first and second
    derivatives, so it's periodic — the seam closes cleanly.
    """
    verts = []
    for i in range(num_curve):
        t = i * 2 * math.pi / num_curve
        # Position
        cx = (math.sin(t) + 2 * math.sin(2 * t)) * major_radius
        cy = (math.cos(t) - 2 * math.cos(2 * t)) * major_radius
        cz = -math.sin(3 * t) * major_radius
        center = np.array([cx, cy, cz])

        # First derivative → tangent
        tx = math.cos(t) + 4 * math.cos(2 * t)
        ty = -math.sin(t) + 4 * math.sin(2 * t)
        tz = -3 * math.cos(3 * t)
        T = np.array([tx, ty, tz])
        T = T / np.linalg.norm(T)

        # Second derivative; Frenet normal is the part perpendicular to T
        ddx = -math.sin(t) - 8 * math.sin(2 * t)
        ddy = -math.cos(t) + 8 * math.cos(2 * t)
        ddz = 9 * math.sin(3 * t)
        D = np.array([ddx, ddy, ddz])
        N = D - np.dot(D, T) * T
        n_len = np.linalg.norm(N)
        if n_len > 1e-9:
            N = N / n_len
        else:
            # Fallback if curvature ≈ 0 (shouldn't happen for the trefoil)
            ref = np.array([0.0, 0.0, 1.0])
            if abs(np.dot(ref, T)) > 0.99:
                ref = np.array([0.0, 1.0, 0.0])
            N = np.cross(T, ref)
            N = N / np.linalg.norm(N)
        B = np.cross(T, N)

        for j in range(num_ring):
            phi = j * 2 * math.pi / num_ring
            verts.append(center + minor_radius
                         * (math.cos(phi) * N + math.sin(phi) * B))

    faces = []
    for i in range(num_curve):
        ip = (i + 1) % num_curve
        for j in range(num_ring):
            jp = (j + 1) % num_ring
            a = i * num_ring + j
            b = i * num_ring + jp
            c = ip * num_ring + jp
            d = ip * num_ring + j
            # Frenet ring axes order makes [a, b, c, d] the outward winding
            faces.append([a, b, c, d])
    return np.array(verts), faces


def generate_stellated_octahedron():
    """Stella octangula — compound of two interpenetrating tetrahedra."""
    verts = np.array([
        # Tetrahedron A
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1],
        # Tetrahedron B
        [-1, -1, -1], [-1, 1, 1], [1, -1, 1], [1, 1, -1],
    ], dtype=float)
    faces = [
        # Tet A
        [0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2],
        # Tet B (winding reversed so its 4 faces point outward)
        [6, 5, 4], [7, 6, 4], [5, 7, 4], [6, 7, 5],
    ]
    return verts, faces
