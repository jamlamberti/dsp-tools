import sys
_ON_PYTHON3 = sys.version_info >= (3, 0)


class CircularBufferIterator(object):
    def __init__(self, cb):
        self._cb = cb
        self._index = 0

    def next(self):
        if self._index > self._cb.buf_sz:
            raise StopIteration
        self._index += 1
        return self._cb.get(self._index - 1)

    def __next__(self):
        return self.next()

class CircularBuffer(object):
    def __init__(self, buf_sz, initial_values=None, initial_value=0):
        self.buf_sz = buf_sz
        self._write_ptr = 0

        if initial_values is None:
            self._buffer = [initial_value for _ in range(buf_sz)]
        else:
            if len(initial_values) != self.buf_sz:
                raise ValueError('Must specify all initial values')
            self._buffer = [x for x in initial_values]
        self._initial_values = [x for x in self._buffer]

    def append(self, val):
        self._buffer[self._write_ptr] = val
        self._write_ptr = (self._write_ptr + 1) % self.buf_sz

    def __getitem__(self, idx):
        return self.get(idx)

    def __iter__(self):
        return CircularBufferIterator(self)

    def get(self, idx):
        actual_idx = (self._write_ptr - 1 - idx) % self.buf_sz
        return self._buffer[actual_idx]

    def flush(self):
        # XXX: flush is probably the wrong thing
        self._buffer = [x for x in self._initial_values]