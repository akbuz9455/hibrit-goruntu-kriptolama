import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
import time

def pixelManipulation(image):
    print("Difüzyona başladı...")
    [row, col, dim] = image.dimension

    alpha = image.matrix[:,:,3]

    #Görüntü boyutunu kullanarak Henon haritası oluşturun
    start_time = time.perf_counter()
    henon_map = generateHenonMap(image)
    elapsed_time = time.perf_counter() - start_time
    print(f"Geçen Zaman: {elapsed_time:0.4f} saniye")
    
    start_time = time.perf_counter()
    resultant_matrix = []
    image_matrix_rgb = []
    
    #Henon haritasını ve görüntü matrisini kanal başına düzleştirin
    henon_map_flatten = henon_map.flatten()
    for i in range(3):
        image_matrix_rgb.append(image.matrix[:,:,i].flatten())
    
    #Her kanal için Henon Haritası ve Görüntü Matrisi arasında XOR işlemini gerçekleştirin
    for i in range(3):
        resultant_matrix.append(np.bitwise_xor(henon_map_flatten, image_matrix_rgb[i])) 
    resultant_matrix = np.asarray(resultant_matrix)

    #Reconstruct the image matrix to its original shape
    resultant_matrix_b = np.reshape(resultant_matrix[0], [row,col])
    resultant_matrix_g = np.reshape(resultant_matrix[1], [row,col])
    resultant_matrix_r = np.reshape(resultant_matrix[2], [row,col])
    resultant_matrix = np.dstack((resultant_matrix_b, resultant_matrix_g, resultant_matrix_r, alpha))
    elapsed_time = time.perf_counter() - start_time
    print(f"Geçen Zaman: {elapsed_time:0.4f} saniye")

    return resultant_matrix

def generateHenonMap(image):
    x = image.key.henon.x
    y = image.key.henon.y
    [row, col, dim] = image.dimension
    sequence_size = row * col * 8
    bit_sequence = [] #dizi 8 bit içerir
    byte_array = []
    for i in range(sequence_size):
        #Henon map formula
        xN = y + 1 - 1.4 * x**2
        yN = 0.3 * x
        
        #xN ve yN yeni x ve y olur
        x = xN
        y = yN

        #Eşik değerini kullanarak ikiliye dönüştürün
        if xN <= 0.3992:
            bit = 0
        else:
            bit = 1
        #bit_sequence'e bit ekle
        try:
            # bit_sequence = np.append(bit_sequence, bit)
            bit_sequence.append(bit)
        except:
            bit_sequence = [bit]
        # ondalık sayıya dönüştür
        if i % 8 == 7:
            decimal = dec(bit_sequence)
            try:
                # byte_array = np.append(byte_array, decimal)
                byte_array.append(decimal)
            except:
                byte_array = [decimal]
            bit_sequence = []
    byte_array = np.asarray(byte_array)
    henon_map = np.reshape(byte_array, [row, col])
    return henon_map

def dec(bitSequence):
    decimal = 0
    for bit in bitSequence:
        decimal = decimal * 2 + int(bit)
    return decimal