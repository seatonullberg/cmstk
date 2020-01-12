from cmstk.visualization.multivariate import parallel_coordinates_plot
import numpy as np
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating parallel coordinates plot...")
    start = datetime.now()

    # prepare plot data
    orange_data = np.random.normal(size=(25, 5))
    blue_data = np.random.normal(size=(25, 5))
    green_data = np.random.normal(size=(25, 5))
    data = [orange_data, blue_data, green_data]
    colors = ["#f47a42", "#4268f4", "#28a83f"]
    labels = ["orange", "blue", "green"]
    xlabels = ["x0", "x1", "x2", "x3", "x4"]
    fig, axes = parallel_coordinates_plot(data, colors, labels, xlabels)
    # customize the plot
    title = "Test Title"
    ylabel = "Test Y Label"
    for i, ax in enumerate(axes):
        ax.set_ylim((-3, 3))
    fig.suptitle(title)
    axes[0].set_ylabel(ylabel)
    # generate the plot
    print("Writing parallel coordinates plot to file...")
    filename = "parallel_coordinates.png"
    fig.savefig(filename, bbox_inches="tight")

    end = datetime.now()
    total_time = (end-start).total_seconds()
    size = os.path.getsize(filename)
    print("Total time: {} seconds".format(total_time))
    print("Generated {} ({} bytes)".format(filename, size))
