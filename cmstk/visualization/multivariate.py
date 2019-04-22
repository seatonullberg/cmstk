import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


class ParallelCoordinatesPlot(object):
    """Represents a plotting object which handles multidimensional coordinates.

    Args:
        title (str): Title of the plot.
        xlabels (list): Name of each quantity on the x axis.
        ylabel (str): Y axis label.

    Attributes:
        custom (dict): Stores custom settings to tweak the plot.
    """

    def __init__(self, title, xlabels, ylabel):
        if type(title) is not str:
            raise TypeError("`title` must be of type str")
        if type(xlabels) is not list:
            raise TypeError("`xlabels` must be of type list")
        if type(ylabel) is not str:
            raise TypeError("`ylabel` must be of type str")

        self._title = title
        self._xlabels = xlabels
        self._ylabel = ylabel

        self._data = []  # list of numpy arrays to plot (can be appended multiple times before plotting) 
        self._colors = []  # list of colors to use when plotting elements of self._data
        self._labels = []  # labels to refer to each dataset by
        self._ncols = None  # the number of columns set by first data addition
        self.custom = {"ylim": None,
                       "legend_loc": "upper right",
                       "plot_origin_line": True}

    def add_data(self, data, color, label):
        """Add a dataset to be plotted in a unique color.
        
        Args:
            data (numpy.ndarray): A 2D array of costs.
            - each addition must have an identical number of columns.
            color (obj): Color to use when plotting all rows of `data`.
            - refer to https://matplotlib.org/users/colors.html for valid inputs.
            label (str): Identifier to include in the plot legend.
        """
        if type(data) is not np.ndarray:
            raise TypeError("`data` must be of type numpy.ndarray")
        if type(label) is not str:
            raise TypeError("`label` must be of type str")

        ncols = data.shape[1]
        if self._ncols is None:
            self._ncols = ncols
        if self._ncols != ncols:
            raise ValueError("`data` must have {} columns".format(self._ncols))
        
        self._data.append(data)
        self._colors.append(color)
        self._labels.append(label)

    def generate_plot(self, filename):
        """Generates and saves a plot to file.

        Args:
            filename (str): File path to write the plot to.
        """
        if type(filename) is not str:
            raise TypeError("`filename` must be of type str")

        fig, axes = plt.subplots(nrows=1, ncols=self._ncols-1, figsize=(8,4), sharey=True)

        x = range(self._ncols)
        patches = []
        # iterate over the axes
        for i, ax in enumerate(axes):
            # iterate over datasets and their corresponding colors/labels
            for dataset, color, label in zip(self._data, self._colors, self._labels):
                # only add legend on the first axis
                if i == 0:
                    patch = mpatches.Patch(color=color, label=label)
                    patches.append(patch)
                # add data to plot
                for d in dataset:
                    ax.plot(x, d, color=color)
                # plot central reference line is desired
                if self.custom["plot_origin_line"]:
                    ax.plot(x, [0 for _ in x], color="black")
            # set custom view port
            if self.custom["ylim"]:
                ax.set_ylim(self.custom["ylim"])
            # alter the xtick labels and style
            ax.set_xlim((x[i], x[i+1]))
            ax.set_xticks([x[i]], minor=False)
            ax.set_xticklabels([self._xlabels[i]])

        # set the last tick label
        axes[-1].set_xticks(x[-2:], minor=False)
        axes[-1].set_xticklabels(self._xlabels[-2:])

        axes[0].set_ylabel(self._ylabel)
        plt.legend(handles=patches, loc=self.custom["legend_loc"])
        fig.suptitle(self._title)

        plt.subplots_adjust(wspace=0)
        plt.savefig(filename)
