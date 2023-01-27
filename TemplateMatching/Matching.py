import os
from tkinter import filedialog
import tkinter
import cv2 as cv
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
from Etiquetado_TM import *

def matching_car(files,path_templates,img_gray):
    for j in files:
        template = cv.imread(path_templates+"/"+j,0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)

        threshold = 0.55
        threshold1 = 0.5

        aux=False
        aux_1=False

        loc = np.where( res >= threshold)
        loc_1 = np.where((res >= threshold1) & (res < threshold))

        pick_car=[]
        pick_car_1=[]

        matching_filter=[]
        matching_filter_1=[]

        if np.shape(loc)[1]:
            aux=True
            point=np.asarray([[loc[1][i],loc[0][i],loc[1][i]+w,loc[0][i]+h] for i in range(np.shape(loc)[1])])
            matching=np.asarray([res[point[i][1]][point[i][0]] for i in range(np.shape(loc)[1])])
            pick = non_max_suppression(point, probs = matching, overlapThresh = 0.1)
            matching_f=np.asarray([res[pick[i][1]][pick[i][0]] for i in range(np.shape(pick)[0])])

            if np.shape(pick_car)[0]==0:
                pick_car=pick
                matching_filter=matching_f
            else:
                pick_car = np.concatenate((pick_car,pick))
                matching_filter = np.concatenate((matching_filter,matching_f))

        if np.shape(loc_1)[1]:
            aux_1=True
            point_1=np.asarray([[loc_1[1][i],loc_1[0][i],loc_1[1][i]+w,loc_1[0][i]+h] for i in range(np.shape(loc_1)[1])])
            matching_1=np.asarray([res[point_1[i][1]][point_1[i][0]] for i in range(np.shape(loc_1)[1])])
            pick_1 = non_max_suppression(point_1, probs = matching_1, overlapThresh = 0.1)
            matching_f_1=np.asarray([res[pick_1[i][1]][pick_1[i][0]] for i in range(np.shape(pick_1)[0])])

            if np.shape(pick_car_1)[0]==0:
                pick_car_1=pick_1
                matching_filter_1=matching_f_1
            else:
                pick_car_1 = np.concatenate((pick_car_1,pick_1))
                matching_filter_1 = np.concatenate((matching_filter,matching_f))

    if aux:
        pick_car = non_max_suppression(pick_car, probs = matching_filter, overlapThresh = 0.1)
        matching_filter=np.asarray([res[pick_car[i][1]][pick_car[i][0]] for i in range(np.shape(pick_car)[0])])
        matching_filter=matching_filter.reshape(len(matching_filter),1)
        identifier=np.asarray([1]*len(matching_filter))
        identifier=identifier.reshape(len(matching_filter),1)
        pick_car=np.concatenate((pick_car, matching_filter, identifier),axis=1)

    if aux_1:
        pick_car_1 = non_max_suppression(pick_car_1, probs = matching_filter_1, overlapThresh = 0.1)
        matching_filter_1=np.asarray([res[pick_car_1[i][1]][pick_car_1[i][0]] for i in range(np.shape(pick_car_1)[0])])
        matching_filter_1=matching_filter_1.reshape(len(matching_filter_1),1)
        identifier=np.asarray([1]*len(matching_filter_1))
        identifier=identifier.reshape(len(matching_filter_1),1)
        pick_car_1=np.concatenate((pick_car_1, matching_filter_1,identifier),axis=1)
    
    return pick_car,pick_car_1

def matching_bus(files,path_templates,img_gray):
    for j in files:
        template = cv.imread(path_templates+"/"+j,0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    
        threshold = 0.475
        threshold1 = 0.425

        aux=False
        aux_1=False

        loc = np.where( res >= threshold)
        loc_1 = np.where((res >= threshold1) & (res < threshold))

        pick_bus=[]
        pick_bus_1=[]

        matching_filter=[]
        matching_filter_1=[]

        if np.shape(loc)[1]:
            aux=True
            point=np.asarray([[loc[1][i],loc[0][i],loc[1][i]+w,loc[0][i]+h] for i in range(np.shape(loc)[1])])
            matching=np.asarray([res[point[i][1]][point[i][0]] for i in range(np.shape(loc)[1])])
            pick = non_max_suppression(point, probs = matching, overlapThresh = 0.1)
            matching_f=np.asarray([res[pick[i][1]][pick[i][0]] for i in range(np.shape(pick)[0])])

            if np.shape(pick_bus)[0]==0:
                pick_bus=pick
                matching_filter=matching_f
            else:
                pick_bus = np.concatenate((pick_bus,pick))
                matching_filter = np.concatenate((matching_filter,matching_f))

        if np.shape(loc_1)[1]:
            aux_1=True
            point_1=np.asarray([[loc_1[1][i],loc_1[0][i],loc_1[1][i]+w,loc_1[0][i]+h] for i in range(np.shape(loc_1)[1])])
            matching_1=np.asarray([res[point_1[i][1]][point_1[i][0]] for i in range(np.shape(loc_1)[1])])
            pick_1 = non_max_suppression(point_1, probs = matching_1, overlapThresh = 0.1)
            matching_f_1=np.asarray([res[pick_1[i][1]][pick_1[i][0]] for i in range(np.shape(pick_1)[0])])

            if np.shape(pick_bus_1)[0]==0:
                pick_bus_1=pick_1
                matching_filter_1=matching_f_1
            else:
                pick_bus_1 = np.concatenate((pick_bus_1,pick_1))
                matching_filter_1 = np.concatenate((matching_filter_1,matching_f_1))
        
    if aux:
        pick_bus = non_max_suppression(pick_bus, probs = matching_filter, overlapThresh = 0.1)
        matching_filter=np.asarray([res[pick_bus[i][1]][pick_bus[i][0]] for i in range(np.shape(pick_bus)[0])])
        matching_filter=matching_filter.reshape(len(matching_filter),1)
        identifier=np.asarray([2]*len(matching_filter))
        identifier=identifier.reshape(len(matching_filter),1)
        pick_bus=np.concatenate((pick_bus, matching_filter,identifier),axis=1)

    if aux_1:
        pick_bus_1 = non_max_suppression(pick_bus_1, probs = matching_filter_1, overlapThresh = 0.1)
        matching_filter_1=np.asarray([res[pick_bus_1[i][1]][pick_bus_1[i][0]] for i in range(np.shape(pick_bus_1)[0])])
        matching_filter_1=matching_filter_1.reshape(len(matching_filter_1),1)
        identifier=np.asarray([2]*len(matching_filter_1))
        identifier=identifier.reshape(len(matching_filter_1),1)
        pick_bus_1=np.concatenate((pick_bus_1, matching_filter_1,identifier),axis=1)
    
    return pick_bus,pick_bus_1

def matching_pedestrian(files,path_templates,img_gray):
    for j in files:
        template = cv.imread(path_templates+"/"+j,0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)

        threshold = 0.29
        threshold1 = 0.275

        aux=False
        aux_1=False

        loc = np.where( res >= threshold)
        loc_1 = np.where((res >= threshold1) & (res < threshold))

        pick_ped=[]
        pick_ped_1=[]

        matching_filter=[]
        matching_filter_1=[]

        if np.shape(loc)[1]:
            aux=True
            point=np.asarray([[loc[1][i],loc[0][i],loc[1][i]+w,loc[0][i]+h] for i in range(np.shape(loc)[1])])
            matching=np.asarray([res[point[i][1]][point[i][0]] for i in range(np.shape(loc)[1])])
            pick = non_max_suppression(point, probs = matching, overlapThresh = 0.1)
            matching_f=np.asarray([res[pick[i][1]][pick[i][0]] for i in range(np.shape(pick)[0])])

            if np.shape(pick_ped)[0]==0:
                pick_ped=pick
                matching_filter=matching_f
            else:
                pick_ped = np.concatenate((pick_ped,pick))
                matching_filter = np.concatenate((matching_filter,matching_f))

        if np.shape(loc_1)[1]:
            aux_1=True
            point_1=np.asarray([[loc_1[1][i],loc_1[0][i],loc_1[1][i]+w,loc_1[0][i]+h] for i in range(np.shape(loc_1)[1])])
            matching_1=np.asarray([res[point_1[i][1]][point_1[i][0]] for i in range(np.shape(loc_1)[1])])
            pick_1 = non_max_suppression(point_1, probs = matching_1, overlapThresh = 0.1)
            matching_f_1=np.asarray([res[pick_1[i][1]][pick_1[i][0]] for i in range(np.shape(pick_1)[0])])

            if np.shape(pick_ped_1)[0]==0:
                pick_ped_1=pick_1
                matching_filter_1=matching_f_1
            else:
                pick_ped_1 = np.concatenate((pick_ped_1,pick_1))
                matching_filter_1 = np.concatenate((matching_filter_1,matching_f_1))

    if aux:
        pick_ped = non_max_suppression(pick_ped, probs = matching_filter, overlapThresh = 0.1)
        matching_filter=np.asarray([res[pick_ped[i][1]][pick_ped[i][0]] for i in range(np.shape(pick_ped)[0])])
        matching_filter=matching_filter.reshape(len(matching_filter),1)
        identifier=np.asarray([3]*len(matching_filter))
        identifier=identifier.reshape(len(matching_filter),1)
        pick_ped=np.concatenate((pick_ped, matching_filter,identifier),axis=1)

    if aux_1:
        pick_ped_1 = non_max_suppression(pick_ped_1, probs = matching_filter_1, overlapThresh = 0.1)
        matching_filter_1=np.asarray([res[pick_ped_1[i][1]][pick_ped_1[i][0]] for i in range(np.shape(pick_ped_1)[0])])
        matching_filter_1=matching_filter_1.reshape(len(matching_filter_1),1)
        identifier=np.asarray([3]*len(matching_filter_1))
        identifier=identifier.reshape(len(matching_filter_1),1)
        pick_ped_1=np.concatenate((pick_ped_1, matching_filter_1,identifier),axis=1)
    
    return pick_ped,pick_ped_1