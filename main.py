import os
import cv2
from skimage.feature import graycomatrix, graycoprops
from components.structural_and_statistical_processing import structural_and_statistical_processing
from components.glcm_processing import glcm_processing
from components.process_images_for_glcm import process_images_for_glcm

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

process_images_for_glcm(letters)

for letter in letters:
    structural_and_statistical_processing(letter)
    glcm_processing(letter)