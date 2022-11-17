import numpy as np


def read_header_hdas(headers: np.ndarray):
    trigger = int(headers[6] / headers[15] / headers[98])
    spatial_sampling_meters=int(headers[1])
    fiber_ref_start = int(headers[17] + 1)
    fiber_ref_stop = int(headers[19] + 1)
    resolution = headers[8]
    decimate = 1
    points = int(headers[14] - headers[12])
    fiber_offset = int(headers[11] / resolution)
    length = headers[13]
    sqrt_ref_fibre_length = int(
        np.floor(np.sqrt(fiber_ref_stop - fiber_ref_start + 1)))
    total_segment = np.array(range(int(fiber_ref_start),
                                   int(sqrt_ref_fibre_length ** 2) +
                                   int(fiber_ref_start))) - 1
    peak_search_window_size = headers[5] * 8 / (1 + headers[9])
    response = {'trigger': trigger, 'fiber_ref_start': fiber_ref_start,
                'fiber_ref_stop': fiber_ref_stop,
                'resolution': resolution, 'decimate': decimate,
                'points': points, 'fiber_offset': fiber_offset,
                'length': length,
                'sqrt_ref_fibre_length': sqrt_ref_fibre_length,
                'total_segment': total_segment,
                'peak_search_window_size': peak_search_window_size,
                'spatial_sampling_meters':spatial_sampling_meters}
    return response

def read_header_energy_hdas(headers: np.ndarray):
    trigger = int(1000 / headers[24])
    fiber_ref_start = int(headers[17] + 1)
    fiber_ref_stop = int(headers[19] + 1)
    time_stamp = float(headers[100])
    decimate = 1
    points = int(headers[14] - headers[12])
    fiber_offset = int(headers[11])
    length = headers[13]
    sqrt_ref_fibre_length = int(
        np.floor(np.sqrt(fiber_ref_stop - fiber_ref_start + 1)))
    total_segment = np.array(range(int(fiber_ref_start),
                                   int(sqrt_ref_fibre_length ** 2) +
                                   int(fiber_ref_start))) - 1
    peak_search_window_size = headers[5] * 8 / (1 + headers[9])
    response = {'trigger': trigger, 'fiber_ref_start': fiber_ref_start,
                'fiber_ref_stop': fiber_ref_stop, 'decimate': decimate,
                'points': points, 'fiber_offset': fiber_offset,
                'length': length,
                'sqrt_ref_fibre_length': sqrt_ref_fibre_length,
                'total_segment': total_segment,
                'peak_search_window_size': peak_search_window_size,
                'time_stamp': time_stamp}
    return response


def read_hdas_data_energy(file_name: str):
    file_open = open(file_name, "rb")
    header = np.fromfile(file_open,
                         count=200,
                         dtype=np.float64)
    header_dict = read_header_energy_hdas(headers=header)

    traces = np.fromfile(file_open,
                         dtype=np.float64)

    read_traces = len(traces) / header_dict['points']
    traces = traces.reshape((int(read_traces), header_dict['points']))
    file_open.close()

    hdas_dict = read_header_energy_hdas(header)
    hdas_dict['traces'] = traces

    return hdas_dict

def read_hdas_data(file_name: str):
    file_open = open(file_name, "rb")
    header = np.fromfile(file_open,
                         count=200,
                         dtype=np.float64)
    header_dict = read_header_hdas(headers=header)

    traces = np.fromfile(file_open,
                         dtype=np.int16)

    read_traces = len(traces) / header_dict['points']
    traces = traces.reshape((int(read_traces), header_dict['points']))
    file_open.close()

    hdas_dict = read_header_hdas(header)
    hdas_dict['traces'] = traces

    return hdas_dict

