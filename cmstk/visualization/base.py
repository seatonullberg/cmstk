import type_sanity as ts
import matplotlib.pyplot as plt


class BasePlot(object):
    """Wrapper for a matplotlib figure.
    
    Args:
        *args, **kwargs
        - passed into plt.subplots()
    
    Attributes:
        fig (pyplot.Figure): The underlying figure.
        axes (list of pyplot.Axes): The underlying axes.
    """

    def __init__(self, *args, **kwargs):
        self.fig, self.axes = plt.subplots(*args, **kwargs)

    def savefig(self, *args, **kwargs):
        self.fig.savefig(*args, **kwargs)

    def suptitle(self, *args, **kwargs):
        self.fig.suptitle(*args, **kwargs)
