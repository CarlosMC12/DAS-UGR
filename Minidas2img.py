from tkinter import filedialog
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from granada.DAS_Format_reference import *

tk.Tk().withdraw()
path_bbdd = filedialog.askdirectory()
files_bbdd = os.listdir(path_bbdd)
print(files_bbdd)

for j in files_bbdd:
    if j[0] != "l":
        das = readDAS(j, apply_scaling=False)
        datas = das["meta"]["energy_data"]
        cm = plt.get_cmap('viridis')
        datas = cm(datas)
        pil_image=Image.fromarray((datas[:, :, :3] * 255).astype(np.uint8))
        path="C:/Users/usuario/Desktop/TESTMINIDAS/"+j+".jpg"
        pil_image.save(path)

        height = pil_image.size[0] 
        width = pil_image.size[1]
        new_p = pil_image.resize((height ,width*11))
        new_p.show()