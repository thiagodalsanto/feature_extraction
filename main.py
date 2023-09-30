import os
from components.structural_and_statistical_processing import structural_and_statistical_processing
from components.glcm_processing import glcm_processing

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for letter in letters:
    structural_and_statistical_processing(letter)
    glcm_processing(letter)
