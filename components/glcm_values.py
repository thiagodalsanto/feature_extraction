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

    # fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    # fig.suptitle(f"Métricas GLCM para {prefix}", fontsize=16)

    # axes[0].imshow(image, cmap="gray")
    # axes[0].set_title("Imagem Original")

    # axes[1].imshow(glcm[:, :, 0, 0], cmap="gray", extent=(0, 1, 0, 1))
    # axes[1].set_title("Matriz GLCM")

    # for ax in axes:
    #     ax.axis("off")

    # plt.savefig(os.path.join(glcm_values_folder, f"{prefix}_glcm_metrics.png"), dpi=300)
    # plt.close(fig)
