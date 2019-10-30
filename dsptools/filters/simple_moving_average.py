from .ccde_filter import CCDEFilter


class SimpleMovingAverage(CCDEFilter):
    def __init__(self, num_points, generator):
        super(SimpleMovingAverage, self).__init__(
            [1. / num_points for _ in range(num_points)], [1.], generator)
