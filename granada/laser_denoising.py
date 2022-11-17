import numpy as np
from granada.hdas_reader import read_hdas_data


def vector_ref_fiber(fiber_ref_stop, fiber_ref_start) -> tuple:
    sqrt_ref_fibre_length = np.floor(np.sqrt(fiber_ref_stop - fiber_ref_start + 1))
    total_segment = np.array(range(int(fiber_ref_start),
                             int(sqrt_ref_fibre_length * sqrt_ref_fibre_length) +
                             int(fiber_ref_start)))

    return int(sqrt_ref_fibre_length), total_segment.astype(int).transpose()


def laser_denoising(input_matrix: np.ndarray,
                    strain_reference: np.ndarray = None,
                    previous_strain: np.ndarray = None,
                    ref_fibre_Length: int = None,
                    total_segment: np.ndarray = None) -> tuple:
    """
    Laser Denoising Using Reference Fiber (2nd order correction, if Ref Update
        Denoise is activated)

    :parameter input_matrix:
    :parameter total_segment:
    :parameter strain_reference:
    :parameter previous_strain:
    :parameter ref_fibre_Length:

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

    return (np.multiply(Data2, 28.8),
            strain_reference_matrix[:, - 1].copy(),
            previous_strain.copy())