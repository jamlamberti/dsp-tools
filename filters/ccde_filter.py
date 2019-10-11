from signal_generators.base_generator import BaseGenerator
from core.circular_buffer import CircularBuffer


class CCDEFilter(BaseGenerator):
    def __init__(self, num_coef, denom_coef, generator):
        super(CCDEFilter, BaseGenerator).__init__()
        self._generator = generator
        if len(num_coef) == 0:
            raise ValueError('Need to specify coefficients')
        if len(denom_coef) == 0:
            denom_coef = [1.]
        self._num_coef = num_coef
        self._denom_coef = denom_coef
        # num has a bias, and current
        # denom is all taps
        self._num_taps = max(len(num_coef), len(denom_coef)) - 1
        if denom_coef[0] != 1.:
            raise ValueError('Output should be 1')
        self._denom_coef = denom_coef[1:]
        self._buf = CircularBuffer(self._num_taps)

    def next_value(self):
        cur_input = self._generator.next_value()
        output_response = sum(
            [coef * self._buf[i] for i, coef in enumerate(self._denom_coef)])
        input_response = sum(
            [coef * self._buf[i] for i, coef in enumerate(self._num_coef)
                if i != 0])
        first_half = cur_input + output_response
        self._buf.append(first_half)

        return (first_half) * self._num_coef[0] + input_response

    def rewind(self):
        self._buf.flush()
        self._generator.rewind()
