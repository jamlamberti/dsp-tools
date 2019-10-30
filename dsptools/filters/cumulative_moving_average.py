from ..signal_generators.base_generator import BaseGenerator


class CumulativeMovingAverage(BaseGenerator):
    def __init__(self, generator):
        super(CumulativeMovingAverage, self).__init__()
        self._generator = generator
        self._cntr = 0
        self._cma = 0.

    def next_value(self):
        self._cntr += 1
        self._cma += float(self._generator.next_value() - self._cma)
        self._cma /= self._cntr
        return self._cma

    def rewind(self):
        self._cntr = 0
        self._cma = 0.
        self._generator.rewind()
