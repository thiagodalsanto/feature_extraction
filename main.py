import os
from components.structural_and_statistical_processing import structural_and_statistical_processing
from components.glcm_processing import glcm_processing
from components.process_images_for_glcm import process_images_for_glcm
from components.structural_statistical_text import structural_statistical_text

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# process_images_for_glcm(letters)
structural_statistical_text(letters)

for letter in letters:
    # structural_and_statistical_processing(letter)
    # glcm_processing(letter)
    pass