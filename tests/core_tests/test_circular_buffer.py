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