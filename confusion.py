import numpy as np
import cv2

def generateArnoldMap(image):
    print("Karışıklık Matrisi Başlatılıyor..")
    N = image.dimension[0]
    # başlangıç ​​değerleri p, q, and iterasyon
    # p ve q değerleri her yinelemede her zaman değiştirilecektir
    p_all = image.key.arnold.p
    q_all = image.key.arnold.q
    iter = image.key.arnold.iter
    
    # piksel konumu için x ve y oluşturun
    x,y = np.meshgrid(range(N),range(N))
    arnold_map = image.matrix
    for i in range(iter):
        # her yineleme için p ve q alın
        p = int(p_all[i%len(p_all)]+p_all[(i+1)%len(p_all)])
        q = int(q_all[i%len(q_all)]+q_all[(i+1)%len(q_all)])
        # Yeni pozisyon için meshgrid oluşturun
        xmap = (x+y*p) % N
        ymap = (x*q+y*(p*q+1)) % N
        arnold_map[xmap,ymap] = arnold_map[x,y]

    return arnold_map

def reconstructArnoldMap(image):
    print("Karışıklık Matrisi Çözülüyor...")
    N = image.dimension[0]
    # başlangıç ​​değerleri p, q ve yineleme
    # p ve q değerleri her yinelemede her zaman değiştirilecektir
    p_all = image.key.arnold.p
    q_all = image.key.arnold.q
    iter = image.key.arnold.iter

    # piksel konumu için x ve y oluşturun
    x,y = np.meshgrid(range(N),range(N))
    arnold_map = image.matrix
    for i in reversed(range(iter)):
        # her yineleme için p ve q alın
        p = int(p_all[i%len(p_all)]+p_all[(i+1)%len(p_all)])
        q = int(q_all[i%len(q_all)]+q_all[(i+1)%len(q_all)])
        # yeni pozisyon için meshgrid oluştur
        xmap = (x+y*p) % N
        ymap = (x*q+y*(p*q+1)) % N
        arnold_map[x,y] = arnold_map[xmap,ymap]

    return arnold_map