# This module contains code for generation of some parametric 3D meshes.

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
