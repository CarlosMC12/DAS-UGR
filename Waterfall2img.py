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

    cm = plt.get_cmap('viridis')
    matrix = cm(matrix)
    pil_image=Image.fromarray((matrix[:, :, :3] * 255).astype(np.uint8))

    path="C:/Users/usuario/Desktop/TESTMINIDAS/A"+j[:-4]+".jpg"
    pil_image.save(path)