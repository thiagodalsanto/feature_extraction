import os
import cv2
from components.glcm_values import glcm_values
from components.structural_statistical_text import structural_statistical_text

def process_images_for_glcm(letters):
    glcm_values_list = []
    
    structural_statistical_text(letters)

    with open("results_statistical_structural.txt", "r") as result_file:
        structural_results = [tuple(map(float, line.strip().split())) for line in result_file]

    for letter in letters:
        for i in range(1, 101):
            archive_name = f"{letter}{i:05d}.pgm"
            image_path = os.path.join("MAIUSCULAS", archive_name)
            if os.path.exists(image_path):
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                resized_image = cv2.resize(image, (200, 200))
                values = glcm_values(resized_image)

                combined_values = values + structural_results.pop(0)
                glcm_values_list.append(combined_values)

            else:
                print(f"Arquivo {archive_name} não encontrado.")

    with open("glcm_metrics.txt", 'w') as f:
        for values in glcm_values_list:
            f.write(f"{values[0]} {values[1]} {values[2]} {values[3]} {values[4]} {values[5]} {' '.join(map(str, values[6:]))}\n")
