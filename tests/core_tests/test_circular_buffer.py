import random
from core.circular_buffer import CircularBuffer


def test_circular_buffer():
    cb_size = 10
    cb = CircularBuffer(cb_size)
    for i in range(cb_size):
        cb.append(i)
        for j in range(i + 1):
            assert cb[j] == i - j


def test_initial_value():
    cb_size = 10
    init_val = 5
    cb = CircularBuffer(cb_size, initial_value=init_val)
    for i in range(cb_size):
        assert cb[i] == init_val

    # Test the flush
    for _ in range(cb_size):
        cb.append(random.random())

    for i in range(cb_size):
        assert cb[i] != init_val

    cb.flush()
    for i in range(cb_size):
        assert cb[i] == init_val


def test_iterating_over_buffer():
    cb_size = 10
    init_val = 5
    cb = CircularBuffer(cb_size, initial_value=init_val)
    for val in cb:
        assert val == init_val


def test_bad_init_length():
    cb_size = 10
    init_val = [i for i in range(cb_size - 1)]
    
    try:
        cb = CircularBuffer(cb_size, initial_values=init_val)
    except ValueError:
        pass
    else:
        raise ValueError('Failed to raise exception')


def test_initial_values():
    cb_size = 10
    init_val = [i for i in range(cb_size)]
    cb = CircularBuffer(cb_size, initial_values=init_val)
    for idx, val in enumerate(cb):
        assert val == init_val[cb_size - idx - 1]


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


def test_next():
    buf_sz = 10
    circ_buf = CircularBuffer(buf_sz, initial_values=list(range(buf_sz)))
    cb_iter = circ_buf.__iter__()
    cnt = 0
    while True:
        try:
            val = cb_iter.next()
        except StopIteration:
            break
        else:
            assert buf_sz - 1 - (cnt % buf_sz) == val
            cnt += 1
            if cnt > buf_sz * 2:
                break
