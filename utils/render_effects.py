# This module contains functions to render effects on images, such as transitioning between images


# Trying to do this with opencv for now
import cv2
import numpy as np
import os


def blend_images(image1, image2, alpha):
    """
    Blend two images together using a specified alpha value.
    
    Parameters:
    image1 : ndarray
        First image.
    image2 : ndarray
        Second image.
    alpha : float
        Blending factor (0.0 to 1.0).
        
    Returns:
    blended_image : ndarray
        Blended image.
    """
    # Ensure the images are the same size
    if image1.shape != image2.shape:
        raise ValueError("Images must be the same size for blending.")
    
    # Blend the images
    blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
    
    return blended_image

def blend_image_sequence(image_sequence1, image_sequence2):
    """
    Blend two sequences of images together using a specified alpha value.
    
    Parameters:
    image_sequence1 : list of ndarray
        First image sequence.
    image_sequence2 : list of ndarray
        Second image sequence.
        
    Returns:
    blended_sequence : list of ndarray
        Blended image sequence.
    """
    blended_sequence = []
    alpha_step = 1.0 / len(image_sequence1)
    alpha = 0.0
    for i in range(len(image_sequence1)):
        blended_image = blend_images(image_sequence1[i], image_sequence2[i], alpha)
        blended_sequence.append(blended_image)
        alpha += alpha_step
    
    return blended_sequence

def blend_images_for_frames(image1, image2, num_frames):
    """
    Blend two images together for a specified number of frames.
    
    Parameters:
    image1 : ndarray
        First image.
    image2 : ndarray
        Second image.
    num_frames : int
        Number of frames to blend over.
        
    Returns:
    blended_sequence : list of ndarray
        Blended image sequence.
    """
    blended_sequence = []
    alpha_step = 1.0 / num_frames
    alpha = 0.0
    for i in range(num_frames):
        blended_image = blend_images(image1, image2, alpha)
        blended_sequence.append(blended_image)
        alpha += alpha_step
    
    return blended_sequence




def blend_image_directories(dir1, dir2, output_dir):
    """
    Blend images from two directories and save the blended images to an output directory.
    
    Parameters:
    dir1 : str
        Path to the first image directory.
    dir2 : str
        Path to the second image directory.
    output_dir : str
        Path to the output directory.
        
    Returns:
    None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files1 = sorted(os.listdir(dir1))
    files2 = sorted(os.listdir(dir2))
    
    for file1, file2 in zip(files1, files2):
        if file1.endswith('.png') and file2.endswith('.png'):
            img1 = cv2.imread(os.path.join(dir1, file1))
            img2 = cv2.imread(os.path.join(dir2, file2))
            blended_image = blend_images(img1, img2, 0.5)
            cv2.imwrite(os.path.join(output_dir, f'blended_{file1}'), blended_image)