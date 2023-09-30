import cv2
import os
import numpy as np
import math
from scipy.stats import kurtosis
import matplotlib.pyplot as plt
from components.fast_glcm import fast_glcm_dissimilarity, fast_glcm_homogeneity, fast_glcm_contrast, fast_glcm_ASM
from components.thinning import thinning 

def structural_and_statistical_processing(letra):
    image_folder = "MAIUSCULAS"
    result_folder = "RESULTADO_ESTRUTURAIS_ESTATISTICAS"

    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    for i in range(1, 26):
        archive_name = f"{letra}{i:05d}.pgm"
        image_path = os.path.join(image_folder, archive_name)

        if os.path.exists(image_path):
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            resized_image = cv2.resize(image, (200, 200))

            _, binarized = cv2.threshold(resized_image, 128, 255, cv2.THRESH_BINARY_INV)

            skeleton = thinning(binarized)

            contours, _ = cv2.findContours(binarized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_image = np.zeros_like(resized_image)
            cv2.drawContours(contours_image, contours, -1, (255, 255, 255), 1)

            resultado = cv2.hconcat([skeleton, contours_image])

            mean = np.mean(image)
            std_deviation = np.std(image)
            curtose = kurtosis(image.flatten())

            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            hist /= hist.sum()
            entropy = -np.sum(np.multiply(hist, np.log2(hist + np.finfo(float).eps)))

            text = f"\nLetra: {letra}\nMedia: {mean:.2f}\nDesvio Padrao: {std_deviation:.2f}\nCurtose: {curtose:.2f}\nEntropia: {entropy:.2f}"

            result_with_text = np.zeros((335, 400), dtype=np.uint8)
            result_with_text[:200, :] = resultado

            font = cv2.FONT_HERSHEY_SIMPLEX
            text_lines = text.split('\n')
            for j, line in enumerate(text_lines):
                cv2.putText(result_with_text, line, (10, 220 + j * 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imwrite(os.path.join(result_folder, f"{letra}{i:05d}_skeleton_contours.png"), result_with_text)
        else:
            print(f"Arquivo {archive_name} não encontrado.")
