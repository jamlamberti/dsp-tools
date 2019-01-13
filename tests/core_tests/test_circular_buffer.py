from dsptools.core.circular_buffer import CircularBuffer


def test_default_value():
    buf_sz = 10
    circ_buf = CircularBuffer(buf_sz, initial_value=1)
    for i in range(buf_sz):
        assert 1 == circ_buf.get(i)


def test_default_value():
    buf_sz = 10
    circ_buf = CircularBuffer(buf_sz, initial_values=list(range(buf_sz)))
    for i in range(buf_sz):
        assert buf_sz - 1 - i == circ_buf.get(i)
