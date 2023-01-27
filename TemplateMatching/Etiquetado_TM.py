import math
import os
import cv2
import numpy as np
from granada.hdas_reader import *
#from granada.laser_denoising import *
from granada.DAS_Format_reference import *
from laser_denosing_with_discontinuity_minization import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import matplotlib.pyplot as plt
import easygui as eg
from datetime import datetime, timedelta
import pathlib


import tkinter as tk
from PIL import Image, ImageTk


def extract_pattern(points,j,tags,bool):
    target_file=j[1:-5]+".bin"
    fichero="C:/Users/usuario/Documents/MATLAB/Scripts_Aragon/Energy_Maps/"+target_file #Energy files directory
    hdas_dict = read_hdas_data_energy(fichero)
    count=0

    for i in points:
        start=(i[0],int(i[1]))
        end=(i[2],int(i[3]))

        matrix = hdas_dict['traces']
        matrix = matrix.transpose()
        matrix = matrix[490:]

        delay=0
        if j[-5]=="1":
            delay=int(np.shape(matrix)[1]/2)

        matrix = matrix[int(i[1]):int(i[3]),int(i[0])+delay:int(i[2])+delay]
        matrix = matrix**2
        energy_matrix=matrix

        cm = plt.get_cmap('viridis')
        matrix = cm(matrix)
        pil_image=Image.fromarray((matrix[:, :, :3] * 255).astype(np.uint8))

        height = pil_image.size[0] 
        width = pil_image.size[1]
        new_p = pil_image.resize((height ,width))
        plt.imshow(new_p)
        plt.ion()
        plt.show()

        if not bool:
            choices = ["Car","Pedestrian","Bus","Pedestrian_Cross","Vertical_Pattern","Undefined_Pattern","Silence","Earthquake","Superconductor"]
            msg = "Pattern detected with low threshold, manually select the detected pattern from the list below\n\nSource file: " + target_file
            reply = eg.buttonbox(msg,"Selección de patrón", choices = choices)
        else:
            reply=tags[count]

        plt.close()

        if reply=="Pedestrian_Cross":
            tag="PC"
        else:
            tag=reply[0]

        temporal_delay = hdas_dict['time_stamp']
        actual_temporal_delay = temporal_delay-2082844800#delay de 66 años=2082844800
        seconds_start=start[0]
        seconds_end=end[0]

        date_event_start=datetime.fromtimestamp(actual_temporal_delay+seconds_start)
        date_event_start_hour=str(date_event_start)[11:19]
        date_event_start_hour_delta = datetime.strptime(date_event_start_hour,"%H:%M:%S")
        date_event_start_hour_delta = timedelta(hours=date_event_start_hour_delta.hour, minutes=date_event_start_hour_delta.minute, seconds=date_event_start_hour_delta.second)

        date_event_end=datetime.fromtimestamp(actual_temporal_delay+seconds_end)
        date_event_end_hour=str(date_event_end)[11:19]
        date_event_end_hour_delta = datetime.strptime(date_event_end_hour,"%H:%M:%S")
        date_event_end_hour_delta = timedelta(hours=date_event_end_hour_delta.hour, minutes=date_event_end_hour_delta.minute, seconds=date_event_end_hour_delta.second)

        date_event_long=date_event_end-date_event_start

        date_event_start_full=date_event_start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        date_event_start_day=date_event_start_full[0:4]+'_'+date_event_start_full[5:7]+'_'+date_event_start_full[8:10]
        date_event_start_full2=date_event_start.strftime('%Y-%m-%d %H.%M.%S.%f')[:-4]
        date_event_start_day_minidas=date_event_start_full2[0:4]+'_'+date_event_start_full2[5:7]+'_'+date_event_start_full2[8:10]+'_'+date_event_start_full2[11:22]
        path=str(pathlib.Path(__file__).parent.resolve())
        path=path[:-6]+date_event_start_day#erase [:-6] if script is running in main folder

        files = os.listdir(path)
        files_hours_start=[]
        for i in files:
            t = datetime.strptime(i[11:20],"%Hh%Mm%Ss")
            delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            time_difference=delta-date_event_start_hour_delta
            files_hours_start.append(time_difference.total_seconds())
        
        res=[ele for ele in files_hours_start if ele < 0]
        file_index_event_start = res.index(res[-1])
        n_seconds_start = abs(files_hours_start[file_index_event_start])

        files_hours_end=[]
        for i in files:
            t = datetime.strptime(i[11:20],"%Hh%Mm%Ss")
            delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            time_difference=delta-date_event_end_hour_delta
            files_hours_end.append(time_difference.total_seconds())
        
        res1=[ele for ele in files_hours_end if ele > 0]
        file_index_event_end = len(files_hours_end)-len(res1)

        files_indexed = file_index_event_end - file_index_event_start
        data_2D = []
        for n in range(files_indexed):
            file_path = path+"\\"+files[file_index_event_start+n]
            hdas_strain_dict = read_hdas_data(file_path)
            matrix = hdas_strain_dict['traces']
            matrix = matrix.transpose()
            if n == 0:
                data_2D = matrix
            else:
                data_2D = np.concatenate((data_2D,matrix), axis = 1)


        previous_strain = None
        strain_reference = None
        data_matrix_buffer = None

        strain, strain_reference, previous_strain, data_matrix_buffer = laser_denoising(
            input_matrix=matrix.transpose(),
            strain_reference=strain_reference,
            previous_strain=previous_strain,
            ref_fibre_Length=hdas_dict["sqrt_ref_fibre_length"],
            total_segment=hdas_dict["total_segment"],
            data_matrix_buffer=data_matrix_buffer
        )

        Trigger_Frequency = hdas_strain_dict["trigger"]
        Strain_time_start = n_seconds_start*Trigger_Frequency
        Strain_time_stop = (n_seconds_start + date_event_long.total_seconds())*Trigger_Frequency
        Strain_meters_start = 490+10+math.floor(start[1])
        Strain_meters_end = 490+10+math.ceil(end[1])


        Trimmed_Strain = strain[Strain_meters_start:Strain_meters_end,int(Strain_time_start):int(Strain_time_stop)]

        fname = tag+date_event_start_day_minidas+".minidas"
        traces = Trimmed_Strain
        data_units = "mk"
        scale_factor = 10
        units_after_scaling = "nstrain"

        epoch = datetime.utcfromtimestamp(0)
        start_time = (date_event_start-epoch).total_seconds()*10e8
        start_time = np.array([start_time], dtype=np.uint64)
        

        sampling_rate = Trigger_Frequency
        gauge_length = hdas_strain_dict["spatial_sampling_meters"]
        latitudes = 0
        longitudes = 0
        elevations = 0

        meters = {"meter_start":Strain_meters_start*10, "meter_end":Strain_meters_end*10}
        diccionario = {"label":reply, "energy_data":energy_matrix,"fiber_meters":meters}

        writeDAS(fname,  traces, data_units, scale_factor, units_after_scaling, start_time, sampling_rate, gauge_length, latitudes, longitudes, elevations, meta=diccionario)
        infoDAS(fname,meta=True)

        count=count+1

