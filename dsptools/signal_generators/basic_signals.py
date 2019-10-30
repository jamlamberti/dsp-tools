from .base_generator import BaseGenerator


class Dirac(BaseGenerator):
    def __init__(self, shift=0):
        super(Dirac, self).__init__()
        self._cntr = 0
        self._shift = shift

    def next_value(self):
        ret_val = 0.
        if self._cntr - self._shift == 0:
            ret_val = 1.
        self._cntr += 1
        return ret_val

    def rewind(self):
        self._cntr = 0


class UnitStep(BaseGenerator):
    def __init__(self, shift=0):
        super(UnitStep, self).__init__()
        self._cntr = 0
        self._shift = shift

    def next_value(self):
        ret_val = 0.
        if self._cntr - self._shift >= 0:
            ret_val = 1.
        self._cntr += 1
        return ret_val

    def rewind(self):
        self._cntr = 0


class ExponentialDecay(BaseGenerator):
    def __init__(self, alpha, shift=0):
        super(ExponentialDecay, self).__init__()
        self._cntr = 0
        self._alpha = alpha
        self._shift = shift
        self._alpha_exp = None

    def next_value(self):
        idx = self._cntr - self._shift
        if idx == 0:
            self._alpha_exp = 1.
        elif self._alpha_exp is None:
            self._alpha_exp = self._alpha ** idx
        else:
            self._alpha_exp *= self._alpha
        ret_val = self._alpha_exp if self._cntr - self._shift >= 0 else 0.
        self._cntr += 1
        return ret_val

    def rewind(self):
        self._cntr = 0


class StepNumber(BaseGenerator):
    def __init__(self, ignore_rewinds=False):
        super(StepNumber, self).__init__()
        self._cntr = 0
        self._ignore_rewinds = ignore_rewinds

    def next_value(self):
        ret_val = self._cntr
        self._cntr += 1
        return ret_val

    def rewind(self):
        if not self._ignore_rewinds:
            self._cntr = 0
