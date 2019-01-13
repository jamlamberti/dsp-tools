class CircularBuffer(object):

    def __init__(self, buf_sz, initial_values=None, initial_value=0):
        self._buf_sz = buf_sz
        self._write_ptr = 0
        self._buffer = self._get_default_buf(initial_values, initial_value)
        self._initial_values = self._buffer[:]
        self._it_val = 0

    def _get_default_buf(self, initial_values, initial_value):
        if initial_values is None:
            return [initial_value for _ in range(self._buf_sz)]
        else:
            if len(initial_values) != self._buf_sz:
                raise ValueError('Must specify all initial values')
            return initial_values[:]

    def append(self, val):
        self._buffer[self._write_ptr] = val
        self._write_ptr = (self._write_ptr + 1) % self._buf_sz

    def __getitem__(self, idx):
        return self.get(idx)

    def __iter__(self):
        self._it_val = 0
        return self

    def __next__(self):
        if self._it_val > self._buf_sz:
            raise StopIteration
        self._it_val += 1
        return self.get(self._it_val - 1)

    def next(self):
        return self.__next__()

    def get(self, idx):
        actual_idx = (self._write_ptr - 1 - idx) % self._buf_sz
        return self._buffer[actual_idx]

    def flush(self):
        # XXX: flush is probably the wrong thing
        self._buffer = [x for x in self._initial_values]
