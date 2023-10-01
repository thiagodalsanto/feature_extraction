import cv2
import os
import numpy as np
import math
import matplotlib.pyplot as plt
from components.fast_glcm import fast_glcm_dissimilarity, fast_glcm_homogeneity, fast_glcm_contrast, fast_glcm_ASM

def glcm_processing(letra):
    image_folder = "MAIUSCULAS"
    result_folder = "RESULTADO_GLCM"

    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    for i in range(1, 11):
        archive_name = f"{letra}{i:05d}.pgm"
        image_path = os.path.join(image_folder, archive_name)

        if os.path.exists(image_path):
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            resized_image = cv2.resize(image, (200, 200))

            dissimilarity = fast_glcm_dissimilarity(resized_image)
            homogeneity = fast_glcm_homogeneity(resized_image)
            contrast = fast_glcm_contrast(resized_image)
            ASM_value, energy_value = fast_glcm_ASM(resized_image)

            dissimilarity_scaled = (
                (dissimilarity - dissimilarity.min())
                / (dissimilarity.max() - dissimilarity.min())
                * 255
            )

            fig, axes = plt.subplots(2, 3, figsize=(12, 8))
            fig.suptitle(f"Métricas GLCM para {letra}{i:05d}", fontsize=16)

            axes[0, 0].imshow(resized_image, cmap="gray")
            axes[0, 0].set_title("Imagem Original")

            axes[0, 1].imshow(np.uint8(dissimilarity_scaled), cmap="gray")
            axes[0, 1].set_title("Dissimilarity")

            axes[0, 2].imshow(np.uint8(homogeneity * 255), cmap="gray")
            axes[0, 2].set_title("Homogeneity")

            axes[1, 0].imshow(np.uint8(contrast * 255), cmap="gray")
            axes[1, 0].set_title("Contrast")

            axes[1, 1].imshow(np.uint8(ASM_value * 255), cmap="gray")
            axes[1, 1].set_title("ASM")

            axes[1, 2].imshow(np.uint8(energy_value * 255), cmap="gray")
            axes[1, 2].set_title("Energy")

            for ax in axes.flatten():
                ax.axis("off")

            plt.savefig(
                os.path.join(
                    result_folder, f"{letra}{i:05d}_metricas_glcm.png"), dpi=300
            )

            plt.close(fig)
        else:
            print(f"Arquivo {archive_name} não encontrado.")
