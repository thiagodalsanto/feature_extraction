import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from fast_glcm import (
    fast_glcm_dissimilarity,
    fast_glcm_homogeneity,
    fast_glcm_contrast,
    fast_glcm_ASM,
)

def processar_imagens(letra):
    pasta_imagens = "MAIUSCULAS"
    pasta_resultado2 = "RESULTADO2"

    if not os.path.exists(pasta_resultado2):
        os.makedirs(pasta_resultado2)

    for i in range(1, 2):
        nome_arquivo = f"{letra}{i:05d}.pgm"
        caminho_imagem = os.path.join(pasta_imagens, nome_arquivo)

        if os.path.exists(caminho_imagem):
            imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)

            imagem_redimensionada = cv2.resize(imagem, (200, 200))

            # Calcule as métricas GLCM
            dissimilarity = fast_glcm_dissimilarity(imagem_redimensionada)
            homogeneity = fast_glcm_homogeneity(imagem_redimensionada)
            contrast = fast_glcm_contrast(imagem_redimensionada)
            ASM_value, energy_value = fast_glcm_ASM(imagem_redimensionada)

            # Ajuste a escala dos valores de dissimilarity para o intervalo [0, 255]
            dissimilarity_scaled = (
                (dissimilarity - dissimilarity.min())
                / (dissimilarity.max() - dissimilarity.min())
                * 255
            )

            # Crie uma figura com várias subparcelas
            fig, axes = plt.subplots(2, 3, figsize=(12, 8))
            fig.suptitle(f"Métricas GLCM para {letra}{i:05d}", fontsize=16)

            # Plote as métricas GLCM nas subparcelas
            axes[0, 0].imshow(imagem_redimensionada, cmap="gray")
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

            # Remova os eixos das subparcelas
            for ax in axes.flatten():
                ax.axis("off")

            # Salve a imagem com todas as métricas
            plt.savefig(
                os.path.join(
                    pasta_resultado2, f"{letra}{i:05d}_metricas_glcm.png"), dpi=300
            )

            # Feche a figura
            plt.close(fig)
        else:
            print(f"Arquivo {nome_arquivo} não encontrado.")

# Resto do código permanece o mesmo

letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for letra in letras:
    processar_imagens(letra)
