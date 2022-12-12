import numpy as np
from granada.hdas_reader import *
import scipy.signal as scs


def laser_denoising(
        input_matrix: np.ndarray,
        total_segment: np.ndarray = None,
        strain_reference: np.ndarray = None,
        previous_strain: np.ndarray = None,
        ref_fibre_Length: int = None,
        data_matrix_buffer: np.ndarray = None,
        peak_search_window: int = 5,
) -> tuple:
    """
    Laser Denoising Using Reference Fiber (2nd order correction, if Ref Update
        Denoise is activated)

    :parameter input_matrix:
    :parameter total_segment:
    :parameter strain_reference:
    :parameter previous_strain:
    :parameter ref_fibre_Length:
    :parameter data_matrix_buffer:
    :parameter peak_search_window:

    :return:
    """
    if total_segment is None or ref_fibre_Length is None:
        vector_ref_fiber_ = vector_ref_fiber(fiber_ref_stop=90, fiber_ref_start=4)
        ref_fibre_Length, total_segment = vector_ref_fiber_

    THRESHOLD = 12000
    SUBTRACT_JUMP = 20000
    DIVIDE_VARIATION = 400
    Data = input_matrix.copy()

    ref_updates = np.greater(Data, THRESHOLD)  # data 2d ref updates
    variations = np.add(np.multiply(np.subtract(Data, SUBTRACT_JUMP), ref_updates),
                        np.multiply(Data, ~ref_updates))
    variation_matrix = np.divide(variations, DIVIDE_VARIATION)
    res = np.multiply(variation_matrix, ref_updates)

    if strain_reference is not None:
        res = np.hstack([strain_reference.reshape((len(strain_reference), 1)), res])

    strain_reference_matrix = np.cumsum(res, axis=1)

    if strain_reference is not None:
        strain_reference_matrix = strain_reference_matrix[:, 1:]
        res = res[:, 1:]

    Data = np.subtract(np.add(strain_reference_matrix, variation_matrix), res)

    if previous_strain is None:
        previous_strain = Data[:, 0]

    def do_segmented_mean(x, previous: np.array = previous_strain):
        segmented_mean = np.subtract(np.mean(np.reshape(x[total_segment],
                                                        (ref_fibre_Length,
                                                         ref_fibre_Length)),
                                             axis=1),
                                     np.mean(np.reshape(previous[total_segment],
                                                        (ref_fibre_Length,
                                                         ref_fibre_Length)),
                                             axis=1))
        val = np.subtract(x, np.median(segmented_mean))
        previous[:] = val[:]
        return val

    Data2 = np.apply_along_axis(do_segmented_mean, 0, Data)

    """ peak hopping """
    roll_data = np.roll(Data, shift=-1, axis=0)
    condition_1 = np.greater(np.abs(np.subtract(Data, roll_data)), 2)
    ref_updates = np.greater(np.add(condition_1, ref_updates), 0)

    """ discontinuity minimization """
    data_matrix_updates, data_matrix_buffer = discontinuity_minimization(
        data_matrix=Data2,
        past_lines_input_matrix=data_matrix_buffer,
        peak_search_window=peak_search_window)

    aux_data_update = np.multiply(data_matrix_updates, ref_updates)
    Data2 = np.add(Data2, aux_data_update)

    return (np.multiply(Data2, 28.8),
            strain_reference_matrix[:, - 1].copy(),
            previous_strain.copy(),
            data_matrix_buffer)


def vector_ref_fiber(fiber_ref_stop, fiber_ref_start) -> tuple:
    sqrt_ref_fibre_length = np.floor(np.sqrt(fiber_ref_stop - fiber_ref_start + 1))
    total_segment = np.array(range(int(fiber_ref_start),
                                   int(sqrt_ref_fibre_length * sqrt_ref_fibre_length) +
                                   int(fiber_ref_start)))

    return int(sqrt_ref_fibre_length), total_segment.astype(int).transpose()


def discontinuity_minimization(
        data_matrix: np.ndarray,
        past_lines_input_matrix: np.ndarray = None,
        peak_search_window: int = 5):
    """
    :param data_matrix:
    :param peak_search_window:
    :param past_lines_input_matrix:

    :return:
    """
    if past_lines_input_matrix is None:
        past_lines_input_matrix = data_matrix[:, :peak_search_window]

    data_matrix = np.hstack([past_lines_input_matrix,
                             data_matrix])

    diff_data = np.diff(data_matrix, axis=1)
    shift_data = np.roll(data_matrix, shift=-1, axis=0)

    median_filter_data = scs.medfilt2d(diff_data,
                                       kernel_size=(1, peak_search_window * 2 + 1))

    aux_data = np.subtract(shift_data, data_matrix)

    output_data = np.add(median_filter_data[:, :-(peak_search_window-1)],
                         aux_data[:, :-peak_search_window])

    return output_data, data_matrix[:, -peak_search_window:]


if __name__ == '__main__':
    import time
    """
       Ejemplo de como utilizar el láser denoising 
    """
    time_start = time.time()

    file_name = r'C:\Users\abel\Documents\InputData\HDASPU21021\RawData' \
                r'\CHA3\2020_06_02_16h58m44s_HDAS_2DRawData_Strain.bin'

    """ Leemos todos los datos  """
    hdas_dict = read_hdas_data(file_name)

    """ 
        Estas variables sirven para aplicar el láser denoising, 
    estos parámetros se actualizan cada vez que se llama a la función.
    La primera vez que se llama a la función han de estar en None.  
    Se recomienda utilizar esta función utilizando datos de un archivo .bin de 
    raw data, archivo de 1 minuto. 
    """
    previous_strain = None
    strain_reference = None
    data_matrix_buffer = None

    matrix = hdas_dict['traces']

    strain, strain_reference, previous_strain, data_matrix_buffer = laser_denoising(
        input_matrix=matrix.transpose(),
        strain_reference=strain_reference,
        previous_strain=previous_strain,
        ref_fibre_Length=hdas_dict["sqrt_ref_fibre_length"],
        total_segment=hdas_dict["total_segment"],
        data_matrix_buffer=data_matrix_buffer
    )

    print('ha leido el primer archivo')
    """
    La segunda vez que llamemos a la función utilizaremos los valores de strain_reference, 
    previous_strain y data_matrix_buffer ya están calculados 
    """
    file_name = r'C:\Users\abel\Documents\InputData\HDASPU21021\RawData' \
                r'\CHA3\2020_06_02_16h59m44s_HDAS_2DRawData_Strain.bin'

    hdas_dict_2 = read_hdas_data(file_name)
    matrix = hdas_dict_2['traces']

    strain_2, strain_reference, previous_strain, data_matrix_buffer = laser_denoising(
        input_matrix=matrix.transpose(),
        strain_reference=strain_reference,
        previous_strain=previous_strain,
        ref_fibre_Length=hdas_dict_2["sqrt_ref_fibre_length"],
        total_segment=hdas_dict_2["total_segment"],
        data_matrix_buffer=data_matrix_buffer
    )

    print('ha leido el segundo archivo ')
    print('Elapsed time {}'.format(time.time() - time_start))
    f = 1

    pass
