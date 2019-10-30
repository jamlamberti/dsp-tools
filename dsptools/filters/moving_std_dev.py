import numpy as np
from ..signal_generators.base_generator import BaseGenerator
from ..core.building_blocks import SplitSignal
from ..core.circular_buffer import CircularBuffer
from ..filters.simple_moving_average import SimpleMovingAverage


class MovingStdDev(BaseGenerator):
    def __init__(self, num_points, generator):
        super(MovingStdDev, self).__init__()
        self._generator = SplitSignal(2, generator)
        self._num_points = num_points
        self._sma = SimpleMovingAverage(self._num_points, self._generator)
        self.cur_avg = 0.
        self.variance = 0.
        self._unnorm_variance = 0.
        self._buf = CircularBuffer(self._num_points)

    def next_value(self):
        new_val = self._generator.next_value()
        new_avg = self._sma.next_value()
        # self._unnorm_variance +=  \
        # (new_val - self._buf[-1]) * (new_val - new_avg - self.cur_avg)
        self.cur_avg = new_avg
        self._buf.append(new_val)
        # self.variance = self._unnorm_variance / (self._num_points - 1.)
        self.variance = np.std(list(self._buf))**2
        return self.variance

    def rewind(self):
        self._sma.rewind()
        self._generator.rewind()
        self.cur_avg = 0
        self.variance = 0
        self._unnorm_variance = 0.
        self._buf.flush()
