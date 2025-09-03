# This module contains functions to convert between different coordinate systems and related utilities
# A lot of this was written witth copilot.. I will remove this as I test and refine. 

import numpy as np
from scipy.spatial.transform import Rotation as R # TODO get rid of scipy as a requirement

# need to work this out for generic axis
def cylindrical2cartesian(r, theta, t,axis):
    """Convert cylindrical coordinates to Cartesian coordinates.
    
    Parameters:
    r : float
        Radius.
    theta : float
        Angle in radians.
    t : float
        Height along the axis.
    axis : int
        Axis of rotation (0 for x, 1 for y, 2 for z).
        
    Returns:
    x, y, z : float
        Cartesian coordinates.
    """
    if axis == 0:  # rotation around x-axis
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = t
    elif axis == 1:  # rotation around y-axis
        x = t
        y = r * np.cos(theta)
        z = r * np.sin(theta)
    else:  # rotation around z-axis
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = t
    return x, y, z

def cartesian2cylindrical(x, y, z, axis):
    """Convert Cartesian coordinates to cylindrical coordinates.

    Parameters:
    x, y, z : float
        Cartesian coordinates.
    axis : int
        Axis of rotation (0 for x, 1 for y, 2 for z).

    Returns:
    r, theta, z : float
        Cylindrical coordinates (radius, angle, height).
    """
    if axis == 0:  # rotation around x-axis
        r, theta = cart2polar(y, z)
        return r, theta, x
    elif axis == 1:  # rotation around y-axis
        r, theta = cart2polar(z, x)
        return r, theta, y
    else:  # rotation around z-axis
        r, theta = cart2polar(x, y)
        return r, theta, z

def cart2polar(x, y):
    """
    Convert Cartesian coordinates to polar coordinates.
    
    Parameters:
    x, y : float
        Cartesian coordinates.
        
    Returns:
    r, theta : float
        Polar coordinates (radius, angle).
    """
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta

def polar2cart(r, theta):
    """
    Convert polar coordinates to Cartesian coordinates.
    
    Parameters:
    r : float
        Radius.
    theta : float
        Angle.
        
    Returns:
    x, y : float
        Cartesian coordinates.
    """
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


# convert from cartesian to spherical coordinates
def cart2sphere(x, y, z):
    """
    Convert Cartesian coordinates to spherical coordinates.
    
    Parameters:
    x, y, z : float
        Cartesian coordinates.
        
    Returns:
    r, theta, phi : float
        Spherical coordinates (radius, polar angle, azimuthal angle).
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)  # polar angle
    phi = np.arctan2(y, x)   # azimuthal angle
    return r, theta, phi

# convert from spherical to cartesian coordinates   
def sphere2cart(r, theta, phi):
    """
    Convert spherical coordinates to Cartesian coordinates.
    
    Parameters:
    r : float
        Radius.
    theta : float
        Polar angle.
    phi : float
        Azimuthal angle.
        
    Returns:
    x, y, z : float
        Cartesian coordinates.
    """
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

# Convert from Euler angles to rotation matrix
def euler2rotm(euler):
    """
    Convert Euler angles to rotation matrix.
    
    Parameters:
    euler : array-like
        Euler angles (roll, pitch, yaw).
        
    Returns:
    R : ndarray
        Rotation matrix.
    """
    r = R.from_euler('xyz', euler)
    return r.as_matrix()

# Convert from rotation matrix to Euler angles
def rotm2euler(R):
    """
    Convert rotation matrix to Euler angles.
    
    Parameters:
    R : ndarray
        Rotation matrix.
        
    Returns:
    euler : ndarray
        Euler angles (roll, pitch, yaw).
    """
    r = R.from_matrix(R)
    return r.as_euler('xyz')

# Convert from rotation matrix to quaternion
def rotm2quat(R):
    """
    Convert rotation matrix to quaternion.
    
    Parameters:
    R : ndarray
        Rotation matrix.
        
    Returns:
    q : ndarray
        Quaternion (x, y, z, w).
    """
    r = R.from_matrix(R)
    return r.as_quat()

def etrans2homo(euler,trans):
    """
    Convert Euler angles and translation vector to homogeneous transformation matrix.

    Parameters:

    euler : array-like
        Euler angles

    trans : array-like
        Translation vector
    Returns:
    t_mat : ndarray
        Homogeneous transformation matrix.

    """
    # import pdb;pdb.set_trace()
    rotm = euler2rotm(euler)
    t_mat = np.eye(4)
    t_mat[:3,:3] = rotm
    t_mat[:3,3] = trans 
    return t_mat
