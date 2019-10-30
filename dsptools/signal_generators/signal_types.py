from .base_generator import BaseGenerator
from ..core.circular_buffer import CircularBuffer


class FiniteSupportSignal(BaseGenerator):
    def __init__(self, sig_sz, generator):
        super(FiniteSupportSignal, self).__init__()
        self._sig_sz = sig_sz
        self._generator = generator
        self._cntr = 0
        if self._sig_sz < 1:
            raise ValueError('FiniteSupportSignal needs to have a support > 0')

    def next_value(self):
        if self._cntr < self._sig_sz:
            self._cntr += 1
            return self._generator.next_value()
        return 0.0

    def rewind(self):
        self._cntr = 0
        self._generator.rewind()


class FiniteLengthSignal(BaseGenerator):
    def __init__(self, sig_sz, generator):
        super(FiniteLengthSignal, self).__init__()
        self._sig_sz = sig_sz
        self._generator = generator
        self._cntr = 0
        if self._sig_sz < 1:
            raise ValueError('FiniteLengthSignal needs to have a support > 0')

    def __call__(self, *args, **kwargs):
        while self._cntr < self._sig_sz:
            yield self.next_value(*args, **kwargs)

    def next_value(self, *args, **kwargs):
        self._cntr += 1
        return self._generator.next_value(*args, **kwargs)

    def run(self, *args, **kwargs):
        while self._cntr < self._sig_sz:
            yield self.next_value(*args, **kwargs)

    def rewind(self):
        self._cntr = 0
        self._generator.rewind()


class PeriodicSignal(BaseGenerator):
    def __init__(self, sig_sz, generator):
        self._generator = generator
        self._sig_sz = sig_sz
        self._buffer = CircularBuffer(sig_sz)
        self._cntr = 0
        if self._sig_sz < 1:
            raise ValueError('PeriodicSignal needs to have a period > 0')

    def next_value(self, *args, **kwargs):
        if self._cntr < self._sig_sz:
            val = self._generator.next_value(*args, **kwargs)
            self._buffer.append(val)
        else:
            val = self._buffer[self._sig_sz - (self._cntr % self._sig_sz)]
        self._cntr += 1
        return val

    def rewind(self):
        self._buffer.flush()
        self._generator.rewind()
        self._cntr = 0
