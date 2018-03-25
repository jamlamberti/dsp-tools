import abc


class BaseGenerator(object):
    _METACLASS_ = abc.ABCMeta

    def __init__(self):
        super(BaseGenerator, self).__init__()

    def __call__(self, *args, **kwargs):
        while True:
            yield self.next_value(*args, **kwargs)

    @abc.abstractmethod
    def next_value(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        while True:
            yield self.next_value(*args, **kwargs)

    @abc.abstractmethod
    def rewind(self, *args, **kwargs):
        pass
