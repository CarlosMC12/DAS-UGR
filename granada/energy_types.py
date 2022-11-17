import numpy as np
from granada import LOGGER


def EnergyFFT(data: np.ndarray, TimeWindow: int,
              Hzini: int = 3, Hzend: int = 45,
              overlap: float = 0.5) -> np.ndarray:
    """
    Calcula la energia de una banda frecuencial definida en el
    siguiente intervalo
    [Hzini, Hzend )


    :parameter data: conjunto de datos para calcular el Waterfall
    :parameter TimeWindow: ventana de solapamiento, como es FFT tiene que
        ser del mismo tamaño que la frecuencia de muestreo. Este código no
        contempla ventanas de FFT menores o mayores
    :parameter Hzini: frecuencia inicial para integrar
    :parameter Hzend: frecuencia final para integrar
    :parameter overlap: solapamiento de los datos

    :return: Devuelve la matriz de energía
    """
    LOGGER.debug('[+] Calculating waterfall...')

    NProcessedPoints, NTimeSamples = data.shape

    W = np.hamming(TimeWindow)

    desplazamiento_solape = int(TimeWindow * overlap)
    NTimeWindows = np.floor(NTimeSamples / desplazamiento_solape) - 1

    AcousticEnergyAverage = np.zeros((NProcessedPoints, int(NTimeWindows)))
    hzs = np.array(range(Hzini, Hzend))

    temporalRange = np.array(range(0, int(TimeWindow)))

    for i in range(int(NTimeWindows)):
        ntr = temporalRange + i * desplazamiento_solape
        fltrData = np.multiply(data[:, ntr], W)
        fft = np.fft.fft(fltrData)
        AcousticEnergyAverage[:, i] = np.sum(np.abs(fft[:, hzs]), axis=1)

    return AcousticEnergyAverage
