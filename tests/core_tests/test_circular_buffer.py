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
