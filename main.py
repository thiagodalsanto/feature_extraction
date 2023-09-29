import cv2
import os
import numpy as np
import math
from scipy.stats import kurtosis

def processar_imagens(letra):
    pasta_imagens = "MAIUSCULAS"
    pasta_resultado = "RESULTADO"
    
    if not os.path.exists(pasta_resultado):
        os.makedirs(pasta_resultado)
    
    for i in range(1, 2):
        nome_arquivo = f"{letra}{i:05d}.pgm"
        caminho_imagem = os.path.join(pasta_imagens, nome_arquivo)
        
        if os.path.exists(caminho_imagem):
            imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
            
            imagem_redimensionada = cv2.resize(imagem, (200, 200))
            
            _, binarizada = cv2.threshold(imagem_redimensionada, 128, 255, cv2.THRESH_BINARY_INV)

            esqueleto = thinning(binarizada)
            
            contorno, _ = cv2.findContours(binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contorno_imagem = np.zeros_like(imagem_redimensionada)
            cv2.drawContours(contorno_imagem, contorno, -1, (255, 255, 255), 1)

            # Junte as imagens do esqueleto e do contorno lado a lado (esqueleto à esquerda, contorno à direita)
            resultado = cv2.hconcat([esqueleto, contorno_imagem])

            # Calcule as estatísticas
            media = np.mean(imagem)
            desvio_padrao = np.std(imagem)
            curtose = kurtosis(imagem.flatten())
            
            hist = cv2.calcHist([imagem], [0], None, [256], [0, 256])
            hist /= hist.sum()
            entropia = -np.sum(np.multiply(hist, np.log2(hist + np.finfo(float).eps)))
            
            texto = f"\nLetra: {letra}\nMedia: {media:.2f}\nDesvio Padrao: {desvio_padrao:.2f}\nCurtose: {curtose:.2f}\nEntropia: {entropia:.2f}"
            
            # Aumente a altura da imagem
            resultado_com_texto = np.zeros((335, 400), dtype=np.uint8)
            resultado_com_texto[:200, :] = resultado
            
            # Adicione o texto à imagem abaixo das imagens
            fonte = cv2.FONT_HERSHEY_SIMPLEX
            linhas_texto = texto.split('\n')
            for i, linha in enumerate(linhas_texto):
                cv2.putText(resultado_com_texto, linha, (10, 220 + i * 20), fonte, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
            # Salve a imagem resultante
            cv2.imwrite(os.path.join(pasta_resultado, f"{letra}{i:05d}_esqueleto_contorno.png"), resultado_com_texto)
        else:
            print(f"Arquivo {nome_arquivo} não encontrado.")

def thinning(img):
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)
    ret, img = cv2.threshold(img, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

    return skel

letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for letra in letras:
    processar_imagens(letra)
