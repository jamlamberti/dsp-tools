import pytest
from dsptools.core.circular_buffer import CircularBuffer


def test_default_value():
    buf_sz = 10
    circ_buf = CircularBuffer(buf_sz, initial_value=1)
    for i in range(buf_sz):
        assert 1 == circ_buf.get(i)


def test_default_values():
    buf_sz = 10
    circ_buf = CircularBuffer(buf_sz, initial_values=list(range(buf_sz)))
    for i in range(buf_sz):
        assert buf_sz - 1 - i == circ_buf.get(i)
        assert buf_sz - 1 - i == circ_buf[i]


def test_invalid_size():
    with pytest.raises(ValueError):
        buf_sz = 10
        circ_buf = CircularBuffer(buf_sz, initial_values=list(range(buf_sz - 1)))
        print circ_buf


def test_iteration():
    buf_sz = 10
    circ_buf = CircularBuffer(buf_sz, initial_values=list(range(buf_sz)))
    for idx, item in enumerate(circ_buf):
        assert item == buf_sz - (idx % buf_sz) - 1
        if idx > buf_sz*2:
            break

def test_flush():
    buf_sz = 10
    circ_buf = CircularBuffer(buf_sz, initial_values=list(range(buf_sz)))
    for i in range(buf_sz):
        assert buf_sz - 1 - i == circ_buf[i]

    for i in range(buf_sz):
        circ_buf.append(buf_sz + i)

    for i in range(buf_sz):
        assert buf_sz - 1 - i != circ_buf[i]

    circ_buf.flush()

    for i in range(buf_sz):
        assert buf_sz - 1 - i == circ_buf[i]
