import cv2
import os
import numpy as np
import math
from scipy.stats import kurtosis
from components.fast_glcm import fast_glcm_dissimilarity, fast_glcm_homogeneity, fast_glcm_contrast, fast_glcm_ASM
from components.thinning import thinning

def structural_statistical_text(letras):
    image_folder = "MAIUSCULAS"

    results = []  

    for letra in letras:
        for i in range(1, 101):
            archive_name = f"{letra}{i:05d}.pgm"
            image_path = os.path.join(image_folder, archive_name)

            if os.path.exists(image_path):
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                resized_image = cv2.resize(image, (200, 200))

                _, binarized = cv2.threshold(resized_image, 128, 255, cv2.THRESH_BINARY_INV)

                skeleton = thinning(binarized)

                contours, _ = cv2.findContours(binarized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours_area = cv2.contourArea(contours[0]) if contours else 0

                skeleton_mean = np.mean(skeleton)

                mean = np.mean(image)
                std_deviation = np.std(image)
                curtose = kurtosis(image.flatten())

                hist = cv2.calcHist([image], [0], None, [256], [0, 256])
                hist /= hist.sum()
                entropy = -np.sum(np.multiply(hist, np.log2(hist + np.finfo(float).eps)))

                results.append([skeleton_mean, contours_area, mean, std_deviation, curtose, entropy])