import os
from tkinter import filedialog
import tkinter
import cv2 as cv
import cv2
import numpy as np
from matplotlib import pyplot as plt
from imutils.object_detection import non_max_suppression

tkinter.Tk().withdraw()
path_templates = filedialog.askdirectory(title="Select templates folder")
files_bbdd = os.listdir(path_templates)
#print(files_bbdd)

fichero = filedialog.askopenfilename(title="Select Energy file", filetypes=[('All Files', '*.jpg')])
img_rgb = cv.imread(fichero)
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

for j in files_bbdd:
    template = cv.imread(path_templates+"/"+j,0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    
    threshold = 0.45
    if j[0]=="P":
        threshold = 0.425
    loc = np.where( res >= threshold)
    
    if np.shape(loc)[1]:
        point=np.asarray([[loc[1][i],loc[0][i],loc[1][i]+w,loc[0][i]+h] for i in range(np.shape(loc)[1])])
        #print(point)
        pick = non_max_suppression(point, probs = None, overlapThresh = 0.1)
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(img_rgb, (xA, yA), (xB, yB), (255,0,0), 2)
            #print((str(xA)+"\n"+str(yA)+"\n"+str(xB)+"\n"+str(yB)+"\n"))
            cv.imwrite('C:/Users/usuario/Desktop/Results2/'+j[:-4]+'.png',img_rgb)

    #HAY QUE ESTRAER LAS PROBABILIDADES DE RES Y CREAR UN VECTOR DE PROBABILIDADES PARA LAS COINCIDENCIAS TRAS NMS