import os
from PIL import Image, ImageOps
import numpy as np
import sys


path_bbdd= "C:/Users/usuario/Desktop/Waterfalls"
files_bbdd = os.listdir(path_bbdd)

for j in files_bbdd:
    im=Image.open(path_bbdd+"/"+j)
    im_gray = ImageOps.grayscale(im)
    im_matrix=np.asarray(im_gray)
    print(type(im_matrix))
    print(np.shape(im_matrix)[0])
    zeros=np.zeros((np.shape(im_matrix)[0]+10, np.shape(im_matrix)[1]+10), dtype=int)
    zeros[5:-5,5:-5]=im_matrix
    np.set_printoptions(threshold=sys.maxsize)
    im_save = Image.fromarray(zeros)
    im_save.convert('RGB').save("C:/Users/usuario/Desktop/Templates2/"+j+".jpg")
    #im=im.resize((48,24),Image.Resampling.LANCZOS)
    #path1="C:/Users/usuario/Desktop/Templates/"+j
    #im.save(path1)
    #print(index)