import numpy as np
from signal_generators.base_generator import BaseGenerator
from core.circular_buffer import CircularBuffer


class Adder(BaseGenerator):
    def __init__(self, *generators):
        super(Adder, self).__init__()
        self._generators = generators

    def next_value(self):
        return sum([gen.next_value() for gen in self._generators])

    def rewind(self):
        for gen in self._generators:
            gen.rewind()


class Gain(BaseGenerator):
    def __init__(self, gain, generator):
        super(Gain, self).__init__()
        self._gain = gain
        self._generator = generator

    def next_value(self):
        return self._gain * self._generator.next_value()

    def rewind(self):
        self._generator.rewind()


class Bias(BaseGenerator):
    def __init__(self, bias, generator):
        super(Bias, self).__init__()
        self._bias = bias
        self._generator = generator

    def next_value(self):
        return self._bias + self._generator.next_value()

    def rewind(self):
        self._generator.rewind()


class WeightedAdder(BaseGenerator):
    def __init__(self, weights, generators):
        super(WeightedAdder, self).__init__()
        self._weights = weights
        self._generators = generators

    def next_value(self):
        return sum([weight * gen.next_value()
                    for weight, gen in zip(self._weights, self._generators)])

    def rewind(self):
        for gen in self._generators:
            gen.rewind()


class Multiplier(BaseGenerator):
    def __init__(self, *generators):
        super(Multiplier, self).__init__()
        self._generators = generators

    def next_value(self):
        return reduce(
            lambda x, y: x * y,
            [gen.next_value() for gen in self._generators], 1)

    def rewind(self):
        for gen in self._generators:
            gen.rewind()


class Delay(BaseGenerator):
    def __init__(self, delay_amt, generator):
        super(Delay, self).__init__()
        self._buf = CircularBuffer(delay_amt)
        self._generator = generator

    def next_value(self):
        ret_val = self._buf[-1]
        self._buf.append(self._generator.next_value())
        return ret_val

    def rewind(self):
        self._generator.rewind()
        self._buf.flush()


class SplitSignal(BaseGenerator):
    def __init__(self, num_copies, generator):
        super(SplitSignal, self).__init__()
        self._num_copies = num_copies
        self._generator = generator
        if num_copies < 0:
            raise ValueError('Must produce 0 or more copies')
        self._cntr = 0
        self._cur_val = 0.
        self.__ran = False

    def change_copies(self, delta):
        if self.__ran:
            raise Exception('Cannot change after processing')
        self._num_copies += delta

    def next_value(self):
        if self._num_copies <= 0:
            raise ValueError('Must produce 0 or more copies')
        self.__ran = True
        if self._cntr == 0:
            self._cur_val = self._generator.next_value()
            self._cntr = self._num_copies
        self._cntr -= 1
        return self._cur_val

    def rewind(self):
        self.__ran = False
        self._generator.rewind()
        self._cntr = 0


class ParallelizeSignals(BaseGenerator):
    def __init__(self, *generators):
        super(ParallelizeSignals, self).__init__()
        self._generators = generators

    def next_value(self):
        return [gen.next_value() for gen in self._generators]

    def rewind(self):
        for gen in self._generators:
            gen.rewind()


class LazyParallelizeSignals(BaseGenerator):
    def __init__(self, input_sig):
        super(LazyParallelizeSignals, self).__init__()
        self._generators = []
        self.splitter = SplitSignal(0, input_sig)

    def add_consumer(self, generator, uses_input=True):
        self._generators.append(generator)
        if uses_input:
            self.splitter.change_copies(1)

    def extend_consumers(self, generators, uses_input=True):
        self._generators.extend(generators)
        if uses_input:
            self.splitter.change_copies(len(generators))

    def get_input_generator(self):
        return self.splitter

    def next_value(self):
        return [gen.next_value() for gen in self._generators]

    def rewind(self):
        for gen in self._generators:
            gen.rewind()
        # shouldn't have to do this, each gen will ultimately do this
        self.splitter.rewind()


class Square(BaseGenerator):
    def __init__(self, generator):
        super(Square, self).__init__()
        self._generator = generator

    def next_value(self):
        val = self._generator.next_value()
        return val ** 2

    def rewind(self):
        self._generator.rewind()


class SquareRoot(BaseGenerator):
    def __init__(self, generator):
        super(SquareRoot, self).__init__()
        self._generator = generator

    def next_value(self):
        val = self._generator.next_value()
        return np.sqrt(val)

    def rewind(self):
        self._generator.rewind()


class ParallelToSerial(BaseGenerator):
    def __init__(self, generator):
        super(ParallelToSerial, self).__init__()
        self._generator = generator
        self._cur_val = None
        self._cntr = 0

    def next_value(self):
        if self._cur_val is None or self._cntr >= len(self._cur_val):
            self._cur_val = self._generator.next_value()
            self._cntr = 0
        ret_val = self._cur_val[self._cntr]
        self._cntr += 1
        return ret_val

    def rewind(self):
        self._cntr = 0
        self._cur_val = None
        self._generator.rewind()
# TODO: upsample, downsample, UpDown
# bilinear, etc, double buffering
