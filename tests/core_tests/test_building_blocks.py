from core import building_blocks
from signal_generators import basic_signals
from tests.signal_generators_tests import test_basic_signals


def all_equal(*args):
    for arg1, arg2 in zip(args[:-1], args[1:]):
        if arg1 != arg2:
            return False
    return True


def all_numerically_equal(*args):
    precision=1E-12
    for arg1, arg2 in zip(args[:-1], args[1:]):
        if abs(arg1 - arg2) > precision:
            return False
    return True


def test_adder_gain_bias():
    unit_step = basic_signals.UnitStep()
    upsampled_unit_step = building_blocks.SplitSignal(4, unit_step)
    source1 = building_blocks.Adder(upsampled_unit_step, upsampled_unit_step)
    source2 = building_blocks.Gain(2., upsampled_unit_step)
    source3 = building_blocks.Bias(1., upsampled_unit_step)

    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        for _ in range(test_basic_signals.MAX_STEPS):
            assert all_equal(
                source1.next_value(),
                source2.next_value(),
                source3.next_value())
        source1.rewind()
        source2.rewind()
        source3.rewind()


def test_delay():
    shift = test_basic_signals.get_shift()
    unit_step_shifted = basic_signals.UnitStep(shift=shift)
    unit_step_delayed = building_blocks.Delay(shift, basic_signals.UnitStep())
    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        for _ in range(test_basic_signals.MAX_STEPS):
            assert all_equal(
                unit_step_shifted.next_value(),
                unit_step_delayed.next_value())
        unit_step_shifted.rewind()
        unit_step_delayed.rewind()


def test_weighting():
    # Should be able to chain different signals together with gains and get the
    # same result by using the weighted adder
    shift = test_basic_signals.get_shift()
    step_num = basic_signals.StepNumber()
    sn_delayed = building_blocks.Delay(shift, basic_signals.StepNumber())

    source1 = building_blocks.Adder(
        building_blocks.Gain(2., step_num),
        building_blocks.Gain(3., sn_delayed))

    source2 = building_blocks.WeightedAdder(
        [2., 3.],
        [
            basic_signals.StepNumber(),
            building_blocks.Delay(shift, basic_signals.StepNumber())])

    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        for _ in range(test_basic_signals.MAX_STEPS):
            assert all_equal(source1.next_value(), source2.next_value())

        source1.rewind()
        source2.rewind()


def test_multiplication():
    shift = test_basic_signals.get_shift()
    dirac = basic_signals.Dirac(shift=shift)
    signal = building_blocks.Multiplier(
        basic_signals.UnitStep(),
        basic_signals.Dirac(shift=shift))

    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        for _ in range(test_basic_signals.MAX_STEPS):
            assert all_equal(dirac.next_value(), signal.next_value())

        dirac.rewind()
        signal.rewind()


def test_squaring():
    source1 = building_blocks.Square(basic_signals.StepNumber())
    source2 = building_blocks.Multiplier(
        basic_signals.StepNumber(), basic_signals.StepNumber())

    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        for _ in range(test_basic_signals.MAX_STEPS):
            assert all_equal(source1.next_value(), source2.next_value())

        source1.rewind()
        source2.rewind()
    source3 = basic_signals.StepNumber()
    source4 = building_blocks.SquareRoot(source1)
    source5 = building_blocks.SquareRoot(source2)


    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        for _ in range(test_basic_signals.MAX_STEPS):
            assert all_equal(
                source3.next_value(),
                source4.next_value(),
                source5.next_value())

        source3.rewind()
        source4.rewind()
        source5.rewind()


def test_splitting():
    sig_split = building_blocks.SplitSignal(1, basic_signals.StepNumber())

    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        for _ in range(test_basic_signals.MAX_STEPS):
            assert not all_equal(
                sig_split.next_value(),
                sig_split.next_value())
        sig_split.rewind()
    sig_split.change_copies(1)
    for _ in range(test_basic_signals.MAX_TEARDOWNS):
        for _ in range(test_basic_signals.MAX_STEPS):
            assert all_equal(
                sig_split.next_value(),
                sig_split.next_value())
        sig_split.rewind()
