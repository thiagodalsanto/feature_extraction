import os
import cv2
from skimage.feature import graycomatrix, graycoprops
from components.structural_and_statistical_processing import structural_and_statistical_processing
from components.glcm_processing import glcm_processing
from components.glcm_values import glcm_values

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for letter in letters:
    structural_and_statistical_processing(letter)
    glcm_processing(letter)

    for i in range(1, 11):
        archive_name = f"{letter}{i:05d}.pgm"
        image_path = os.path.join("MAIUSCULAS", archive_name)
        if os.path.exists(image_path):
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(image, (200, 200))
            glcm_values(resized_image, f"{letter}{i:05d}")
        else:
            print(f"Arquivo {archive_name} não encontrado.")