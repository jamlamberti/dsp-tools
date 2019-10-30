import numpy as np
from .base_generator import BaseGenerator


class SineGenerator(BaseGenerator):
    def __init__(self, omega):
        super(SineGenerator, self).__init__()
        self._omega = float(omega)
        self._cntr = 0

    def next_value(self):
        ret_val = np.sin(self._omega * self._cntr)
        self._cntr += 1
        return ret_val

    def rewind(self):
        self._cntr = 0


class CosineGenerator(BaseGenerator):
    def __init__(self, omega):
        super(CosineGenerator, self).__init__()
        self._omega = float(omega)
        self._cntr = 0

    def next_value(self):
        ret_val = np.cos(self._omega * self._cntr)
        self._cntr += 1
        return ret_val

    def rewind(self):
        self._cntr = 0


class SampledSineGenerator(SineGenerator):
    def __init__(self, sampling_freq, signal_freq):
        super(SampledSineGenerator, self).__init__(
            2 * np.pi * signal_freq / sampling_freq)


class SampledCosineGenerator(CosineGenerator):
    def __init__(self, sampling_freq, signal_freq):
        super(SampledCosineGenerator, self).__init__(
            2 * np.pi * signal_freq / sampling_freq)
