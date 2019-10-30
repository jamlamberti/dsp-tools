from .ccde_filter import CCDEFilter


class LeakyIntegrator(CCDEFilter):
    def __init__(self, alpha, generator):
        super(LeakyIntegrator, self).__init__(
            [1 - alpha], [1, alpha], generator)
