import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from granada.hdas_reader import *

path_energy= "C:/Users/usuario/Documents/MATLAB/Scripts_Aragon/Energy_Maps/"
files_bbdd = os.listdir(path_energy)

for j in files_bbdd:
    hdas_dict = read_hdas_data_energy(path_energy+j)
    matrix = hdas_dict['traces']
    matrix = matrix.transpose()
    matrix = matrix[490:]
    print(np.shape(matrix))
    matrix = matrix**2
    print(np.shape(matrix))

    half_index = int((np.shape(matrix)[1]/2))
    matrix0 = matrix[:,:half_index]
    matrix1 = matrix[:,half_index:]

    cm = plt.get_cmap('viridis')
    matrix0 = cm(matrix0)
    pil_image0=Image.fromarray((matrix0[:, :, :3] * 255).astype(np.uint8))
    path0="C:/Users/usuario/Desktop/TESTMINIDAS3/A"+j[:-4]+"0"+".jpg"
    pil_image0.save(path0)

    cm1 = plt.get_cmap('viridis')
    matrix1 = cm1(matrix1)
    pil_image1=Image.fromarray((matrix1[:, :, :3] * 255).astype(np.uint8))
    path1="C:/Users/usuario/Desktop/TESTMINIDAS3/A"+j[:-4]+"1"+".jpg"
    pil_image1.save(path1)

    #cm = plt.get_cmap('viridis')
    #matrix = cm(matrix)
    #pil_image=Image.fromarray((matrix[:, :, :3] * 255).astype(np.uint8))

    #path="C:/Users/usuario/Desktop/TESTMINIDAS2/A"+j[:-4]+".jpg"
    #pil_image.save(path)