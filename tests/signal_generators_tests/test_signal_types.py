from dsptools.signal_generators import signal_types
from dsptools.signal_generators import basic_signals
from tests.signal_generators_tests import test_basic_signals


def test_finite_support_signal_callable():
    shift = test_basic_signals.get_shift()
    unit_step = basic_signals.UnitStep(shift=shift)
    unit_step_fls = signal_types.FiniteLengthSignal(test_basic_signals.MAX_STEPS, unit_step)
    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        sig = list(unit_step_fls())
        assert len(sig) == test_basic_signals.MAX_STEPS
        for idx, val in enumerate(sig):
            assert test_basic_signals.is_unit_step_signal(idx, val, shift)
        unit_step_fls.rewind()

def test_finite_support_signal_run():
    shift = test_basic_signals.get_shift()
    unit_step = basic_signals.UnitStep(shift=shift)
    unit_step_fls = signal_types.FiniteLengthSignal(test_basic_signals.MAX_STEPS, unit_step)
    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        sig = list(unit_step_fls.run())
        assert len(sig) == test_basic_signals.MAX_STEPS
        for idx, val in enumerate(sig):
            assert test_basic_signals.is_unit_step_signal(idx, val, shift)
        unit_step_fls.rewind()

def test_bad_support_FLS():
    unit_step = basic_signals.UnitStep()
    try:
        unit_step_fls = signal_types.FiniteLengthSignal(0, unit_step)
    except ValueError:
        pass
    else:
        raise ValueError("Should have failed due to bad signal length")


def test_finite_support_signal():
    # We can convert a unit step into a dirac by making it have a support of 1
    unit_step = basic_signals.UnitStep()
    dirac = signal_types.FiniteSupportSignal(1, unit_step)
    test_basic_signals.wrap_teardowns(test_basic_signals.is_dirac_signal, dirac)()


def test_bad_support_FSS():
    unit_step = basic_signals.UnitStep()
    try:
        unit_step_fss = signal_types.FiniteSupportSignal(0, unit_step)
    except ValueError:
        pass
    else:
        raise ValueError("Should have failed due to bad signal length")


def test_periodic_signal():
    # we can convert a dirac signal into a unit step by making it periodic over 1 step
    dirac = basic_signals.Dirac()
    unit_step = signal_types.PeriodicSignal(1, dirac)
    test_basic_signals.wrap_teardowns(test_basic_signals.is_unit_step_signal, unit_step)()


def test_period_signal_bad_period():
    unit_step = basic_signals.UnitStep()
    try:
        unit_step_periodic = signal_types.PeriodicSignal(0, unit_step)
    except ValueError:
        pass
    else:
        raise ValueError("Should have failed due to bad period length")
