import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Any, List, Optional, Tuple


def parallel_coordinates_plot(
        data: List[np.ndarray],
        colors: List[Any],
        labels: List[str],
        xlabels: Optional[List[str]] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """Prepares a plot displaying multidimensional coordinates along a continuous axis.

    Args:
        data: Data to plot.
        colors: Color to associate with each dataset.
        labels: Label to associate with each dataset.
        xlabels: Labels to populate the x axis with
    """
    if xlabels is None:
        xlabels = [str(i) for i in range(len(data))]
    if len(data) != len(colors) != len(labels) != len(xlabels):
        err = "size of all inputs must match"
        raise ValueError(err)
    ncols = data[0].shape[1]
    fig, axes = plt.subplots(nrows=1, ncols=ncols - 1, sharey=True)
    x = range(ncols)
    patches = []
    for i, ax in enumerate(axes):
        for dataset, color, label in zip(data, colors, labels):
            if i == 0:
                patch = mpatches.Patch(color=color, label=label)
                patches.append(patch)
            for d in dataset:
                ax.plot(x, d, color=color)
            ax.plot(x, [0 for _ in x], color="black")
        ax.set_xlim((x[i], x[i + 1]))
        ax.set_xticks([x[i]], minor=False)
        ax.set_xticklabels([xlabels[i]])
    axes[-1].set_xticks(x[-2:], minor=False)
    axes[-1].set_xticklabels(xlabels[-2:])
    fig.subplots_adjust(wspace=0)
    fig.legend(handles=patches)
    return (fig, axes)
