import os
from tkinter import filedialog
import tkinter
import cv2 as cv
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
from Etiquetado_TM import *
from Matching import *

tkinter.Tk().withdraw()
path_templates = filedialog.askdirectory(title="Select templates folder")
files_bbdd = os.listdir(path_templates)

path_fichero = filedialog.askdirectory(title="Select Energy file")
files_fichero = os.listdir(path_fichero)

for i in files_fichero:
    img_rgb = cv.imread(path_fichero+"/"+i)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    pick_all=[]
    pick_all_1=[]
    img_rgb_1=img_rgb

    files_bus=[]
    files_car=[]
    files_ped=[]
    for j in files_bbdd:
        if j[0]=="B":
            files_bus=files_bus+list([j])
        if j[0]=="P":
            files_ped=files_ped+list([j])
        if j[0]=="C":
            files_car=files_car+list([j])

    pick_bus,pick_bus_1=matching_bus(files_bus,path_templates,img_gray)
    pick_ped,pick_ped_1=matching_pedestrian(files_ped,path_templates,img_gray)
    pick_car,pick_car_1=matching_car(files_car,path_templates,img_gray)

    if np.shape(pick_bus)[0]==0:pick_bus=np.asarray([[0,0,0,0,0,0]])
    if np.shape(pick_bus_1)[0]==0:pick_bus_1=np.asarray([[0,0,0,0,0,0]])
    if np.shape(pick_ped)[0]==0:pick_ped=np.asarray([[0,0,0,0,0,0]])
    if np.shape(pick_ped_1)[0]==0:pick_ped_1=np.asarray([[0,0,0,0,0,0]])
    if np.shape(pick_car)[0]==0:pick_car=np.asarray([[0,0,0,0,0,0]])
    if np.shape(pick_car_1)[0]==0:pick_car_1=np.asarray([[0,0,0,0,0,0]])

    pick_all = np.concatenate((pick_bus,pick_ped,pick_car))
    pick_all_1 = np.concatenate((pick_bus_1,pick_ped_1,pick_car_1))

    matching=pick_all[:,-2:-1]
    matching_1=pick_all_1[:,-2:-1]

    identifier=pick_all[:,-1]
    identifier_1=pick_all_1[:,-1]

    print(i[1:-4])
    print("Cars = ["+str(np.shape(np.where(identifier == 1))[1])+","+str(np.shape(np.where(identifier_1 == 1))[1])+"]")
    print("Buses = ["+str(np.shape(np.where(identifier == 2))[1])+","+str(np.shape(np.where(identifier_1 == 2))[1])+"]")
    print("Pedestrians = ["+str(np.shape(np.where(identifier == 3))[1])+","+str(np.shape(np.where(identifier_1 == 3))[1])+"]")

    pick_all = pick_all[:,0:-2].astype(int)
    pick_all_1 = pick_all_1[:,0:-2].astype(int)

    for (xA, yA, xB, yB) in pick_all:
        cv2.rectangle(img_rgb, (xA, yA), (xB, yB), (0,255,0), 2)
    cv.imwrite('C:/Users/usuario/Desktop/Results2/'+i[:-4]+'0.png',img_rgb)

    #extract_pattern(pick_all,i,identifier,True)

    for (xA, yA, xB, yB) in pick_all_1:
        cv2.rectangle(img_rgb_1, (xA, yA), (xB, yB), (0,0,255), 2)
    cv.imwrite('C:/Users/usuario/Desktop/Results2/'+i[:-4]+'1.png',img_rgb_1)
    
    #extract_pattern(pick_all_1,i,identifier_1,False)