import os
import diffusion as dif
from PIL import ImageTk, Image
import confusion as con
import reshape as res
import cv2
import Image as i
import time

def decrypt(filepath, destination_path, key):
    im_encrypted = i.Image(filepath, i.Type.ENCRYPTED, cv2.imread(filepath, cv2.IMREAD_UNCHANGED), key)
    print(im_encrypted.filename)

    path = os.path.join('.', 'images')
    
    #Yayılım işlemi başlar başlatırız
    im_undiffused = i.Image(path+"\\undiffused\\"+im_encrypted.filename.split('.')[0]+".png", i.Type.UNDIFFUSED, dif.pixelManipulation(im_encrypted), key)
    #dağılmanın çıktısını kaydetmek için aşağıdaki uncomment kodu
    # cv2.imwrite(im_undiffused.filepath, im_undiffused.matrix)

    #yayılım geri alma işlemi başlar
    start_time = time.perf_counter()
    im_unconfused = i.Image(path+"\\unconfused\\"+im_encrypted.filename.split('.')[0]+".png", i.Type.UNCONFUSED, con.reconstructArnoldMap(im_undiffused), key)
    elapsed_time = time.perf_counter() - start_time
    print(f"Geçen Zaman: {elapsed_time:0.4f} saniye")
    #karışıklığın çıktısını kaydetmek için aşağıdaki uncomment kodu
    # cv2.imwrite(im_unconfused.filepath, im_unconfused.matrix)

    #kırpma kenarlığını yeniden şekillendir
    start_time = time.perf_counter()
    im_decrypted = i.Image(destination_path+"\\"+im_encrypted.filename.split('.')[0]+".png", i.Type.DECRYPTED, res.cropBorder(im_unconfused), key)
    elapsed_time = time.perf_counter() - start_time
    print(f"Geçen Zaman: {elapsed_time:0.4f} saniye")
    cv2.imwrite(im_decrypted.filepath, im_decrypted.matrix)