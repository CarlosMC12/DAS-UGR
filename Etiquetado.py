import math
import os
import numpy as np
from granada.hdas_reader import *
from granada.laser_denoising import *
from granada.DAS_Format_reference import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from PIL import Image
import matplotlib.pyplot as plt
import easygui as eg
from datetime import datetime, timedelta
import pathlib


import tkinter as tk
from PIL import Image, ImageTk


# Variables globales
_start = None    
_end = None
_img = None
_photo = None
_img_path = None
_funcids = {}


def _enable_croping():
    global canvas
    _funcids["<Button-1>"] = canvas.bind("<Button-1>", _on_click, '+')
    _funcids["<B1-Motion>"] = canvas.bind("<B1-Motion>", _on_drag, '+')
    _funcids["<ButtonRelease-1>"] = canvas.bind("<ButtonRelease-1>", _on_drop, '+')

def _disable_croping():
    global canvas
    global crop_btn
    for event, funcid in _funcids.items():
        canvas.unbind(event, funcid)
    crop_btn.config(state="disabled")


def open_image():
    global _img
    global _photo
    global _img_path
    global canvas

    file = new_p
    if not file:
        return None

    canvas.delete("all")
    try:
        _img = new_p
    except OSError:
        _img = None
        _photo = None
        _img_path = None
        _disable_croping()
    else:
        _photo = ImageTk.PhotoImage(_img)
        _img_path = file
        canvas.create_image(0, 0, image=_photo, anchor="nw", tags="image")
        _enable_croping()
    finally:
        canvas.config(scrollregion=canvas.bbox(tk.ALL))


def _on_click(event):
    global _start
    global _end
    global canvas
    _start = (canvas.canvasx(event.x), canvas.canvasy(event.y))
    _end = None

def _on_drop(event):
    global _start
    global _end
    global _img
    global crop_btn

    if _end is None:
        crop_btn.config(state="disabled")

    else:

        # Acotar límites de seleción a la imagen
        img_x, img_y = _img.size

        x0, y0 = _start
        x0 = img_x if x0 > img_x else 0 if x0 < 0 else x0
        y0 = img_y if y0 > img_y else 0 if y0 < 0 else y0 
        _start = (x0, y0)

        x1, y1 = _end
        x1 = img_x if x1 > img_x else 0 if x1 < 0 else x1
        y1 = img_y if y1 > img_y else 0 if y1 < 0 else y1       
        _end = (x1, y1)

        # Normalizado para obtener vertice superior izquierdo e inferior derecho
        if x0 > x1:
            if y0 < y1: # _start es el vértice superior derecho
                _start = (x1, y0)
                _end = (x0, y1)
            else:       # _start es el vértice inferior derecho
                _start, _end = _end, _start
        else:
            if y0 > y1:  # _start es el vértice inferior izquierdo
                _start = (x0, y1)
                _end = (x1, y0)

        crop_btn.config(state="normal")

    # Redibujar rectágulo
    _draw_rectangle()



def _on_drag(event):
    global _start
    global _end
    global canvas

    x0, y0 = _start
    ex, ey = canvas.canvasx(event.x), canvas.canvasy(event.y)
    _end = (ex, ey)
    _draw_rectangle()


def _draw_rectangle():
    global canvas
    global _end
    global _start

    canvas.delete("rectangle")

    if _end is None or _start is None:    
        return None

    x0, y0 = _start
    x1, y1 = _end

    canvas.create_rectangle(x0, y0, x1, y1, fill="#18c194",
                            width=1, stipple="gray50", tags='rectangle'
                            )

def _crop_image():
    global _img
    global _start
    global _end
    global _cropped
    # Recortado de la imagen 
    #print(_start, _end)
    _cropped = _img.crop(_start + _end)
    _extract_pattern()

def _extract_pattern():
    choices = ["Car","Pedestrian","Bus","Pedestrian_Cross","Vertical_Pattern","Undefined_Pattern","Silence","Earthquake","Superconductor"]
    msg = "Seleccione el patrón detectado de la lista a continuación"
    reply = eg.buttonbox(msg,"Selección de patrón", choices=choices)

    if reply=="Pedestrian_Cross":
        tag="PC"
    else:
        tag=reply[0]
    print(reply)
    print(tag)
    print(_start,_end)

    temporal_delay = hdas_dict['time_stamp']
    actual_temporal_delay = temporal_delay-2082844800#delay de 66 años=2082844800
    seconds_start=_start[0]
    seconds_end=_end[0]

    date_event_start=datetime.fromtimestamp(actual_temporal_delay+seconds_start)
    date_event_start_hour=str(date_event_start)[11:19]
    date_event_start_hour_delta = datetime.strptime(date_event_start_hour,"%H:%M:%S")
    date_event_start_hour_delta = timedelta(hours=date_event_start_hour_delta.hour, minutes=date_event_start_hour_delta.minute, seconds=date_event_start_hour_delta.second)

    date_event_end=datetime.fromtimestamp(actual_temporal_delay+seconds_end)
    date_event_end_hour=str(date_event_end)[11:19]
    date_event_end_hour_delta = datetime.strptime(date_event_end_hour,"%H:%M:%S")
    date_event_end_hour_delta = timedelta(hours=date_event_end_hour_delta.hour, minutes=date_event_end_hour_delta.minute, seconds=date_event_end_hour_delta.second)

    date_event_long=date_event_end-date_event_start

    #date_event_start.strftime('%Y-%M-%d %H:%M:%S.%f')[:-4]
    date_event_start_full=date_event_start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    print(date_event_start_full)
    date_event_start_day=date_event_start_full[0:4]+'_'+date_event_start_full[5:7]+'_'+date_event_start_full[8:10]
    date_event_start_full2=date_event_start.strftime('%Y-%m-%d %H.%M.%S.%f')[:-4]
    date_event_start_day_minidas=date_event_start_full2[0:4]+'_'+date_event_start_full2[5:7]+'_'+date_event_start_full2[8:10]+'_'+date_event_start_full2[11:22]
    print(date_event_start_day)
    path=str(pathlib.Path(__file__).parent.resolve())
    path=path[:-6]+date_event_start_day#erase [:-6] if script is running in main folder
    print(path)

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
            print(np.shape(data_2D))
        else:
            data_2D = np.concatenate((data_2D,matrix), axis = 1)
            print(np.shape(data_2D))


    previous_strain = None
    strain_reference = None
    
    strain, strain_reference, previous_strain = laser_denoising(
        data_2D,
        strain_reference,
        previous_strain,
        hdas_strain_dict["sqrt_ref_fibre_length"],
        hdas_strain_dict["total_segment"])

    Trigger_Frequency = hdas_strain_dict["trigger"]
    print(Trigger_Frequency)
    Strain_time_start = n_seconds_start*Trigger_Frequency
    Strain_time_stop = (n_seconds_start + date_event_long.total_seconds())*Trigger_Frequency
    Strain_meters_start = 490+10+math.floor(_start[1]/11)
    Strain_meters_end = 490+10+math.ceil(_end[1]/11)


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

    energy_matrix = matrix[Strain_meters_start:Strain_meters_end,int(seconds_start):int(seconds_end)]
    print(np.shape(matrix))
    print(np.shape(energy_matrix))

    meters = {"meter_start":Strain_meters_start*10, "meter_end":Strain_meters_end*10}
    diccionario = {"label":reply, "energy_data":energy_matrix,"fiber_meters":meters}

    writeDAS(fname,  traces, data_units, scale_factor, units_after_scaling, start_time, sampling_rate, gauge_length, latitudes, longitudes, elevations, meta=diccionario)
    print("finish")
    infoDAS(fname,meta=True)
    das = readDAS(fname, apply_scaling=False)
    restored_energy = das["meta"]["energy_data"]
    print(np.shape(restored_energy))
    #print(Trimmed_Strain)
    #print(np.shape(Trimmed_Strain))
    #print(Strain_meters_end-Strain_meters_start)
    #print(int(Strain_time_stop)-int(Strain_time_start))

    
            


root = tk.Tk()
root.title("Recortar imagen")

# Frame contenedor con canvas y barras de desplazamiento
frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
yscrollbar = tk.Scrollbar(frame)
canvas = tk.Canvas(frame, bd=0,
                   xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set,
                   height=500,width=1000
                   )
#open_btn = tk.Button(root, text="Abrir imagen", command=open_image)
crop_btn = tk.Button(root, text="Recortar imagen", state="disabled", command=_crop_image)


# Estructurando el widget
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
xscrollbar.grid(row=1, column=0, columnspan=2, sticky="ew")
yscrollbar.grid(row=0, column=1, sticky="ns")
canvas.grid(row=0, column=0, sticky="nsew")
#open_btn.grid(row=2, column=0, sticky="ew")
crop_btn.grid(row=2, column=1, sticky="nsew")

xscrollbar.config(command=canvas.xview)
yscrollbar.config(command=canvas.yview)

tk.Tk().withdraw()
fichero = filedialog.askopenfilename(title="Select Energy file", filetypes=[('All Files', '*.bin')])

""" Leemos todos los datos  """
hdas_dict = read_hdas_data_energy(fichero)

""" 
    Estas variables sirven para aplicar el láser denoising, 
estos parámetros se actualizan cada vez que se llama a la función.
La primera vez que se llama a la función han de estar en None.  
Se recomienda utilizar esta función utilizando datos de un archivo .bin de 
raw data, archivo de 1 minuto. 
"""
matrix = hdas_dict['traces']
matrix = matrix.transpose()
matrix = matrix[490:]

cm = plt.get_cmap('viridis')
matrix = cm(matrix)
pil_image=Image.fromarray((matrix[:, :, :3] * 255).astype(np.uint8))

height = pil_image.size[0] 
width = pil_image.size[1]
new_p = pil_image.resize((height ,width*11))

# Inicio del mainloop de la app
open_image()
root.mainloop()