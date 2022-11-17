import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import numpy as np
from granada import LOGGER
import re


def get_datetime(filename):
    result = re.search('[0-9]{4}_[0-9]{2}_[0-9]{2}_[0-9]{2}h[0-9]{2}m[0-9]{2}s', filename)
    if result:
        datatime_string = result.group(0)
        datatime_string = datatime_string.replace('h', '_').replace('m', '_').replace('s', '')
        timestamp_in_millis = datetime.datetime.strptime(datatime_string, "%Y_%m_%d_%H_%M_%S")
        return timestamp_in_millis
    else:
        result = re.search('[0-9]{4}_[0-9]{2}_[0-9]{2}_[0-9]{2}_[0-9]{2}_[0-9]{2}', filename)
        if result:
            datatime_string = result.group(0)
            datatime_string = datatime_string.replace('h', '_').replace('m', '_').replace('s', '')
            timestamp_in_millis = datetime.datetime.strptime(datatime_string, "%Y_%m_%d_%H_%M_%S")
            return timestamp_in_millis
        return 0


def plot_waterfall(nombre_fichero: str, matrix_waterfall: np.ndarray,
                   minimo_rango: float = 0, maximo_rango: float = 600):
    LOGGER.info('[+] Plotting waterfall ... ')
    fig, axs = plt.subplots()
    iniDatefile = get_datetime(nombre_fichero)
    y_lims = [iniDatefile, iniDatefile + datetime.timedelta(seconds=60)]
    y_lims = mdates.date2num(y_lims)
    maxPx = matrix_waterfall.shape[0]
    axs.imshow(matrix_waterfall.transpose(), origin='lower',
               vmin=minimo_rango, vmax=maximo_rango,
               extent=[0, maxPx, y_lims[0], y_lims[1]], aspect='auto')
    axs.yaxis_date()
    axs.set_xlabel('Distance (m)')
    plt.show()

