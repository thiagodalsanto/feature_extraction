import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import graycomatrix, graycoprops
import cv2

def glcm_values(image, prefix):
    glcm_values_folder = "RESULTADO_GLCM_VALUES"

    if not os.path.exists(glcm_values_folder):
        os.makedirs(glcm_values_folder)

    distances = [1]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]

    glcm = graycomatrix(image, distances, angles, symmetric=True, normed=True)

    dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    asm = graycoprops(glcm, 'ASM')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]

    output_file = os.path.join(glcm_values_folder, f"{prefix}_glcm_metrics.txt")

    with open(output_file, 'w') as f:
        f.write(f"Dissimilarity: {dissimilarity}\n")
        f.write(f"Homogeneity: {homogeneity}\n")
        f.write(f"Contrast: {contrast}\n")
        f.write(f"ASM: {asm}\n")
        f.write(f"Energy: {energy}\n")