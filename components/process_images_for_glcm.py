import os
import cv2
from components.glcm_values import glcm_values

def process_images_for_glcm(letters):
    for letter in letters:
        for i in range(1, 11):
            archive_name = f"{letter}{i:05d}.pgm"
            image_path = os.path.join("MAIUSCULAS", archive_name)
            if os.path.exists(image_path):
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                resized_image = cv2.resize(image, (200, 200))
                glcm_values(resized_image, f"{letter}{i:05d}")
            else:
                print(f"Arquivo {archive_name} não encontrado.")
