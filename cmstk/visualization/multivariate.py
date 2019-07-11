import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


class ParallelCoordinatesPlot(object):
    """Implementation of a plot displaying multidimensional coordinates along a 
    continuous axis.
    
    Args:
        ncols (int): The dimensionality of the coordinates.
        xlabels (optional) (list of str): The labels to assign to each 
        dimension.
    """

    def __init__(self, ncols, xlabels=None):
        assert type(ncols) is int
        self._ncols = ncols
        if xlabels is None:
            self._xlabels = [i for i in range(ncols)]
        else:
            self._xlabels = xlabels
        self._data = []    # list of numpy.ndarrays
        self._colors = []  # list of colors to use for each member of self._data
        self._labels = []  # list of labels for each member of self._data
        self.fig, self.axes = plt.subplots(nrows=1, ncols=self._ncols-1,
                                           figsize=(10, 5), sharey=True)

    def add_data(self, data, color, label):
        """Add a dataset to be plotted.
        
        Args:
            data (numpy.ndarray): The data to plot.
            - each addition must have an identical number of columns equal to self._ncols
            color (obj): Color to associate with data.
            - refer to https://matplotlib.org/users/colors.html for valid inputs.
            label (str): label to associate with data.
        """
        assert type(data) is np.ndarray
        assert type(label) is str
        ncols = data.shape[1]
        if ncols != self._ncols:
            raise ValueError("`data` must have {} columns".format(self._ncols))
        self._data.append(data)
        self._colors.append(color)
        self._labels.append(label)

    def make(self):
        """Plots the available data.
        
        Args:
            None
        """
        x = range(self._ncols)
        patches = []
        # iterate over the axes
        for i, ax in enumerate(self.axes):
            # iterate over datasets and their corresponding colors/labels
            for dataset, color, label in zip(self._data, self._colors, self._labels):
                # only add legend on the first axis
                if i == 0:
                    patch = mpatches.Patch(color=color, label=label)
                    patches.append(patch)
                # add data to plot
                for d in dataset:
                    ax.plot(x, d, color=color)
                # plot central reference line
                ax.plot(x, [0 for _ in x], color="black")
            # alter the xtick labels and style
            ax.set_xlim((x[i], x[i+1]))
            ax.set_xticks([x[i]], minor=False)
            ax.set_xticklabels([self._xlabels[i]])

        # set the last tick label
        self.axes[-1].set_xticks(x[-2:], minor=False)
        self.axes[-1].set_xticklabels(self._xlabels[-2:])

        # adjust spacing
        self.fig.subplots_adjust(wspace=0)
        # self.fig.legend moves the legend outside of the axes
        plt.legend(handles=patches, loc="upper right")
