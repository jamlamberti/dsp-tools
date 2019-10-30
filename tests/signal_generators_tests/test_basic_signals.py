from __future__ import division
import random
from dsptools.signal_generators import basic_signals


MAX_TEARDOWNS = 5
MAX_STEPS = 10

def get_shift():
    """Utility func for getting a reasonible shift in MAX_STEPS"""
    return random.randint(MAX_STEPS // 4, MAX_STEPS // 2)


def wrap_teardowns(func, generator):
    def __wrapped_func(*args, **kwargs):
        for _ in range(MAX_TEARDOWNS):
            for idx in range(MAX_STEPS):
                val = generator.next_value()
                assert func(idx, val, *args, **kwargs)
            generator.rewind()
    return __wrapped_func


def is_dirac_signal(idx, val, shift=0):
    if idx != shift:
        return val == 0.
    return val == 1.


def is_unit_step_signal(idx, val, shift=0):
    if idx >= shift:
        return val == 1.
    return val == 0.


def test_dirac():
    # Verify signal is zero in all but one spot and has unit amplitude there
    dirac = basic_signals.Dirac()
    
    wrap_teardowns(is_dirac_signal, dirac)()


def test_dirac_with_shifts():
    # just pick a random offset to go from
    shift = get_shift()
    dirac = basic_signals.Dirac(shift=shift)
    wrap_teardowns(is_dirac_signal, dirac)(shift=shift)


def test_unit_step():
    unit_step = basic_signals.UnitStep()
    wrap_teardowns(is_unit_step_signal, unit_step)()


def test_unit_step_with_shift():
    shift = get_shift()
    unit_step = basic_signals.UnitStep(shift=shift)
    wrap_teardowns(is_unit_step_signal, unit_step)(shift=shift)


def test_exponential_decay_at_1():
    # if alpha is 1, should stay constant @ 1.
    expon_decay = basic_signals.ExponentialDecay(alpha=1.)
    wrap_teardowns(lambda _, val: val == 1., expon_decay)()


def test_exponential_shifted():
    alpha = random.random()
    shift = get_shift()
    expon_decay = basic_signals.ExponentialDecay(alpha=alpha)
    expon_decay_shifted = basic_signals.ExponentialDecay(alpha=alpha, shift=shift)

    for _ in range(MAX_TEARDOWNS):
        for idx in range(MAX_STEPS):
            if idx < shift:
                _ = expon_decay_shifted.next_value()
                continue
            shifted = expon_decay_shifted.next_value()
            zero_centered = expon_decay.next_value()
            assert abs(shifted - zero_centered) < 1E-12
        expon_decay.rewind()
        expon_decay_shifted.rewind()


def test_relative_decay():
    alphas = [random.random()]
    if alphas[0] > 0.5:
        alphas.append(alphas[0] - 0.1)
    else:
        alphas.append(alphas[0] + 0.1)
    a_min = min(alphas)
    a_max = max(alphas)
    ed_min = basic_signals.ExponentialDecay(alpha=a_min)
    ed_max = basic_signals.ExponentialDecay(alpha=a_max)

    for _ in range(MAX_TEARDOWNS):
        for idx in range(MAX_STEPS):
            val_min = ed_min.next_value()
            val_max = ed_max.next_value()
            if idx == 0:
                # weak @ 1.
                assert val_min == val_max
            else:
                # I belive it is a strong bound
                assert val_min < val_max
        ed_min.rewind()
        ed_max.rewind()


def is_step_number_signal(idx, val):
    return idx == val


def test_step_number():
    gen = basic_signals.StepNumber()
    wrap_teardowns(is_step_number_signal, gen)()


def test_step_number_no_rewinds():
    cntr = 0
    gen = basic_signals.StepNumber(ignore_rewinds=True)
    for _ in range(MAX_TEARDOWNS):
        for _ in range(MAX_STEPS):
            assert gen.next_value() == cntr
            cntr += 1
        gen.rewind()
