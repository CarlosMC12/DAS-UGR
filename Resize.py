import os
from PIL import Image

path_bbdd= "C:/Users/usuario/Desktop/Refill"
files_bbdd = os.listdir(path_bbdd)

for j in files_bbdd:
    im=Image.open(path_bbdd+"/"+j)
    im=im.resize((38,14),Image.Resampling.LANCZOS)
    path1="C:/Users/usuario/Desktop/Waterfalls/"+j
    im.save(path1)
    #print(index)